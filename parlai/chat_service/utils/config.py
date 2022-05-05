#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
"""
Config Utils.
"""

import yaml
from collections import namedtuple

from parlai.core.params import ParlaiParser
from parlai.scripts.safe_interactive import setup_args

WorldConfig = namedtuple(
    "WorldConfig",
    [
        "world_name",
        "onboarding_name",
        "task_name",
        "max_time_in_pool",
        "agents_required",
        "backup_task",
    ],
)


def parse_configuration_file(config_path):
    """
    Read the config file for an experiment to get ParlAI settings.

    :param config_path:
        path to config

    :return:
        parsed configuration dictionary
    """
    result = {}
    result["configs"] = {}
    with open(config_path) as f:
        cfg = yaml.load(f.read(), Loader=yaml.SafeLoader)
        # get world path
        result["world_path"] = cfg.get("world_module")
        if not result["world_path"]:
            raise ValueError("Did not specify world module")
        result["overworld"] = cfg.get("overworld")
        if not result["overworld"]:
            raise ValueError("Did not specify overworld")
        result["max_workers"] = cfg.get("max_workers")
        if not result["max_workers"]:
            raise ValueError("Did not specify max_workers")
        result["task_name"] = cfg.get("task_name")
        if not result["task_name"]:
            raise ValueError("Did not specify task name")
        task_world = cfg.get("tasks")
        if task_world is None or len(task_world) == 0:
            raise ValueError("task not in config file")
        # get task file
        for task_name, configuration in task_world.items():
            if "task_world" not in configuration:
                raise ValueError("{} does not specify a task".format(task_name))
            result["configs"][task_name] = WorldConfig(
                world_name=task_name,
                onboarding_name=configuration.get("onboard_world"),
                task_name=configuration.get("task_world"),
                max_time_in_pool=configuration.get("timeout") or 300,
                agents_required=configuration.get("agents_required") or 1,
                backup_task=configuration.get("backup_task"),
            )
        # get world options, additional args
        world_opt = cfg.get("opt",{})
        '''
        for model in world_opt['models']:
            for arg in list(world_opt['models'][model]):
                if '-' in arg:
                    new_arg = arg.replace('-','_')
                    world_opt['models'][model][new_arg] =  world_opt['models'][model].pop(arg)
        
        parser = setup_args()
        parser.add_extra_args(world_opt['models']['multimodal_blenderbot'])
        args = parser.parse_args(args=world_opt['models']['multimodal_blenderbot'])
        for arg in world_opt['models']['multimodal_blenderbot']:
            print(arg)
        args.log()
        '''
        result["world_opt"] = world_opt
        result["additional_args"] = cfg.get("additional_args", {})

    return result
