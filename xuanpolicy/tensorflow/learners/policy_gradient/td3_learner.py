# TD3 add three tricks to DDPG:
# 1. noisy action in target actor
# 2. double critic network
# 3. delayed actor update
from xuanpolicy.tensorflow.learners import *
import itertools


class TD3_Learner(Learner):
    def __init__(self,
                 policy: tk.Model,
                 optimizers: Sequence[tk.optimizers.Optimizer],
                 summary_writer: Optional[SummaryWriter] = None,
                 device: str = "cpu:0",
                 modeldir: str = "./",
                 gamma: float = 0.99,
                 tau: float = 0.01,
                 delay: int = 3):
        self.tau = tau
        self.gamma = gamma
        self.delay = delay
        super(TD3_Learner, self).__init__(policy, optimizers, summary_writer, device, modeldir)

    def save_model(self):
        model_path = self.modeldir + "model-%s-%s" % (time.asctime(), str(self.iterations))
        self.policy.actor.save(model_path)
        self.policy.target_actor.save(model_path)
        self.policy.criticA.save(model_path)
        self.policy.target_criticA.save(model_path)
        self.policy.criticB.save(model_path)
        self.policy.target_criticB.save(model_path)

    def update(self, obs_batch, act_batch, rew_batch, next_batch, terminal_batch):
        self.iterations += 1
        with tf.device(self.device):
            act_batch = tf.convert_to_tensor(act_batch)
            rew_batch = tf.expand_dims(tf.convert_to_tensor(rew_batch), axis=1)
            ter_batch = tf.expand_dims(tf.convert_to_tensor(terminal_batch), axis=1)

            with tf.GradientTape() as tape:
                # critic update
                _, action_q = self.policy.Qaction(obs_batch, act_batch)
                _, target_q = self.policy.Qtarget(next_batch)
                backup = rew_batch + self.gamma * (1 - ter_batch) * target_q
                backup = tf.stop_gradient(tf.reshape(tf.tile(backup, (1, 2)), [-1, ]))

                q_loss = tk.losses.mean_squared_error(backup, tf.reshape(action_q, [-1, ]))
                train_parameters = self.policy.criticA.trainable_variables + self.policy.criticB.trainable_variables
                gradients = tape.gradient(q_loss, train_parameters)
                self.optimizer[1].apply_gradients([
                    (grad, var)
                    for (grad, var) in zip(gradients, train_parameters)
                    if grad is not None
                ])

            with tf.GradientTape() as tape:
                # actor update
                if self.iterations % self.delay == 0:
                    _, policy_q = self.policy.Qpolicy(obs_batch)
                    p_loss = -tf.reduce_mean(policy_q)
                    gradients = tape.gradient(p_loss, self.policy.actor.trainable_variables)
                    self.optimizer[0].apply_gradients([
                        (grad, var)
                        for (grad, var) in zip(gradients, self.policy.actor.trainable_variables)
                        if grad is not None
                    ])
                    self.policy.soft_update(self.tau)

            actor_lr = self.optimizer[0]._decayed_lr(tf.float32)
            critic_lr = self.optimizer[1]._decayed_lr(tf.float32)
            self.writer.add_scalar("Qloss", q_loss.numpy(), self.iterations)
            if self.iterations % self.delay == 0:
                self.writer.add_scalar("Ploss", p_loss.numpy(), self.iterations)
            self.writer.add_scalar("Qvalue", tf.math.reduce_mean(action_q).numpy(), self.iterations)
            self.writer.add_scalar("actor_lr", actor_lr.numpy(), self.iterations)
            self.writer.add_scalar("critic_lr", critic_lr.numpy(), self.iterations)
