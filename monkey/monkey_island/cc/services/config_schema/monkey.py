from monkey_island.cc.services.utils.typographic_symbols import WARNING_SIGN
from common.data.system_info_collectors_names import (AWS_COLLECTOR,
                                                      ENVIRONMENT_COLLECTOR,
                                                      HOSTNAME_COLLECTOR,
                                                      PROCESS_LIST_COLLECTOR)

MONKEY = {
    "title": "Monkey",
    "type": "object",
    "properties": {
        "general": {
            "title": "General",
            "type": "object",
            "properties": {
                "alive": {
                    "title": "Alive",
                    "type": "boolean",
                    "default": True,
                    "description": "Is the monkey alive"
                },
                "post_breach_actions": {
                    "title": "Post breach actions",
                    "type": "array",
                    "uniqueItems": True,
                    "items": {
                        "$ref": "#/definitions/post_breach_actions"
                    },
                    "default": [
                        "BackdoorUser",
                        "CommunicateAsNewUser",
                        "ModifyShellStartupFiles",
                        "HiddenFiles",
                        "TrapCommand",
                        "ChangeSetuidSetgid",
                        "ScheduleJobs"
                    ]
                },
            }
        },
        "behaviour": {
            "title": "Behaviour",
            "type": "object",
            "properties": {
                "custom_PBA_linux_cmd": {
                    "title": "Linux post breach command",
                    "type": "string",
                    "default": "",
                    "description": "Linux command to be executed after breaching."
                },
                "PBA_linux_file": {
                    "title": "Linux post breach file",
                    "type": "string",
                    "format": "data-url",
                    "description": "File to be executed after breaching. "
                                   "If you want custom execution behavior, "
                                   "specify it in 'Linux post breach command' field. "
                                   "Reference your file by filename."
                },
                "custom_PBA_windows_cmd": {
                    "title": "Windows post breach command",
                    "type": "string",
                    "default": "",
                    "description": "Windows command to be executed after breaching."
                },
                "PBA_windows_file": {
                    "title": "Windows post breach file",
                    "type": "string",
                    "format": "data-url",
                    "description": "File to be executed after breaching. "
                                   "If you want custom execution behavior, "
                                   "specify it in 'Windows post breach command' field. "
                                   "Reference your file by filename."
                },
                "PBA_windows_filename": {
                    "title": "Windows PBA filename",
                    "type": "string",
                    "default": ""
                },
                "PBA_linux_filename": {
                    "title": "Linux PBA filename",
                    "type": "string",
                    "default": ""
                },
                "self_delete_in_cleanup": {
                    "title": "Self delete on cleanup",
                    "type": "boolean",
                    "default": True,
                    "description": "Should the monkey delete its executable when going down"
                },
                "use_file_logging": {
                    "title": "Use file logging",
                    "type": "boolean",
                    "default": True,
                    "description": "Should the monkey dump to a log file"
                },
                "serialize_config": {
                    "title": "Serialize config",
                    "type": "boolean",
                    "default": False,
                    "description": "Should the monkey dump its config on startup"
                }
            }
        },
        "system_info": {
            "title": "System info",
            "type": "object",
            "properties": {
                "extract_azure_creds": {
                    "title": "Harvest Azure Credentials",
                    "type": "boolean",
                    "default": True,
                    "attack_techniques": ["T1003"],
                    "description":
                        "Determine if the Monkey should try to harvest password credentials from Azure VMs"
                },
                "collect_system_info": {
                    "title": "Collect system info",
                    "type": "boolean",
                    "default": True,
                    "attack_techniques": ["T1082", "T1005", "T1016"],
                    "description": "Determines whether to collect system info"
                },
                "should_use_mimikatz": {
                    "title": "Should use Mimikatz",
                    "type": "boolean",
                    "default": True,
                    "attack_techniques": ["T1003"],
                    "description": "Determines whether to use Mimikatz"
                },
                "system_info_collector_classes": {
                    "title": "System info collectors",
                    "type": "array",
                    "uniqueItems": True,
                    "items": {
                        "$ref": "#/definitions/system_info_collector_classes"
                    },
                    "default": [
                        ENVIRONMENT_COLLECTOR,
                        AWS_COLLECTOR,
                        HOSTNAME_COLLECTOR,
                        PROCESS_LIST_COLLECTOR
                    ]
                },
            }
        },
        "life_cycle": {
            "title": "Life cycle",
            "type": "object",
            "properties": {
                "max_iterations": {
                    "title": "Max iterations",
                    "type": "integer",
                    "default": 1,
                    "description": "Determines how many iterations of the monkey's full lifecycle should occur"
                },
                "victims_max_find": {
                    "title": "Max victims to find",
                    "type": "integer",
                    "default": 100,
                    "description": "Determines the maximum number of machines the monkey is allowed to scan"
                },
                "victims_max_exploit": {
                    "title": "Max victims to exploit",
                    "type": "integer",
                    "default": 15,
                    "description":
                        "Determines the maximum number of machines the monkey"
                        " is allowed to successfully exploit. " + WARNING_SIGN
                        + " Note that setting this value too high may result in the monkey propagating to "
                          "a high number of machines"
                },
                "timeout_between_iterations": {
                    "title": "Wait time between iterations",
                    "type": "integer",
                    "default": 100,
                    "description":
                        "Determines for how long (in seconds) should the monkey wait between iterations"
                },
                "retry_failed_explotation": {
                    "title": "Retry failed exploitation",
                    "type": "boolean",
                    "default": True,
                    "description":
                        "Determines whether the monkey should retry exploiting machines"
                        " it didn't successfully exploit on previous iterations"
                }
            }
        }
    }
}
