import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from typing import Sequence, Optional, Callable, Union, Dict
from gym.spaces import Space, Box, Discrete, Dict
from torch.utils.tensorboard import SummaryWriter
from argparse import Namespace

from .learner import Learner, LearnerMAS
from .policy_gradient.pg_learner import PG_Learner
from .policy_gradient.a2c_learner import A2C_Learner
from .policy_gradient.ppoclip_learner import PPOCLIP_Learner
from .policy_gradient.ppokl_learner import PPOKL_Learner
from .policy_gradient.ppg_learner import PPG_Learner
from .policy_gradient.ddpg_learner import DDPG_Learner
from .policy_gradient.td3_learner import TD3_Learner
from .policy_gradient.sac_learner import SAC_Learner
from .policy_gradient.sacdis_learner import SACDIS_Learner
from .policy_gradient.pdqn_learner import PDQN_Learner
from .policy_gradient.mpdqn_learner import MPDQN_Learner
from .policy_gradient.spdqn_learner import SPDQN_Learner

from .qlearning_family.dqn_learner import DQN_Learner
from .qlearning_family.dueldqn_learner import DuelDQN_Learner
from .qlearning_family.ddqn_learner import DDQN_Learner
from .qlearning_family.perdqn_learner import PerDQN_Learner
from .qlearning_family.c51_learner import C51_Learner
from .qlearning_family.qrdqn_learner import QRDQN_Learner
from .qlearning_family.cdqn_learner import CDQN_Learner
from .qlearning_family.ldqn_learner import LDQN_Learner
from .qlearning_family.cldqn_learner import CLDQN_Learner

from .multi_agent_rl.iql_learner import IQL_Learner
from .multi_agent_rl.vdn_learner import VDN_Learner
from .multi_agent_rl.qmix_learner import QMIX_Learner
from .multi_agent_rl.wqmix_learner import WQMIX_Learner
from .multi_agent_rl.qtran_learner import QTRAN_Learner
# from .multi_agent_rl.dcg_learner import DCG_Learner
from .multi_agent_rl.vdac_learner import VDAC_Learner
from .multi_agent_rl.coma_learner import COMA_Learner
from .multi_agent_rl.iddpg_learner import IDDPG_Learner
from .multi_agent_rl.maddpg_learner import MADDPG_Learner
from .multi_agent_rl.mfq_learner import MFQ_Learner
from .multi_agent_rl.mfac_learner import MFAC_Learner
from .multi_agent_rl.mappoclip_learner import MAPPO_Clip_Learner
from .multi_agent_rl.mappokl_learner import MAPPO_KL_Learner
from .multi_agent_rl.isac_learner import ISAC_Learner
from .multi_agent_rl.masac_learner import MASAC_Learner
from .multi_agent_rl.madqn_learner import MADQN_Learner
from .multi_agent_rl.matd3_learner import MATD3_Learner
