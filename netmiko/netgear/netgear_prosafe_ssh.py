"""ProSafe OS support"""

import time
from typing import Any

from netmiko.cisco_base_connection import CiscoSSHConnection


class NetgearProSafeSSH(CiscoSSHConnection):
    """ProSafe OS support"""

    def __init__(self, **kwargs: Any) -> None:
        if kwargs.get("default_enter") is None:
            kwargs["default_enter"] = "\r"
        return super().__init__(**kwargs)

    def session_preparation(self) -> None:
        """ProSafe OS requires enable mode to disable paging."""
        self._test_channel_read()
        self.set_base_prompt()
        self.enable()
        self.disable_paging(command="terminal length 0")

        # Clear the read buffer
        time.sleep(0.3 * self.global_delay_factor)
        self.clear_buffer()

    def check_config_mode(
        self,
        check_string: str = "(Config)#",
        pattern: str = "",
        force_regex: bool = False,
    ) -> bool:
        return super().check_config_mode(check_string=check_string, pattern=pattern)

    def config_mode(
        self,
        config_command: str = "configure",
        pattern: str = r"\)\#",
        re_flags: int = 0,
    ) -> str:
        return super().config_mode(
            config_command=config_command, pattern=pattern, re_flags=re_flags
        )

    def exit_config_mode(self, exit_config: str = "exit", pattern: str = r"\#") -> str:
        return super().exit_config_mode(exit_config=exit_config, pattern=pattern)

    def save_config(
        self,
        save_cmd: str = "write memory confirm",
        confirm: bool = False,
        confirm_response: str = "",
    ) -> str:
        self.enable()
        """ProSafe doesn't allow saving whilst within configuration mode"""
        if self.check_config_mode():
            self.exit_config_mode()

        return super().save_config(
            cmd=save_cmd, confirm=confirm, confirm_response=confirm_response
        )

class NetgearProSafeTelnet(NetgearProSafeSSH):
    """ProSafe OS support"""
    def telnet_login(
        self,
        pri_prompt_terminator: str = r"\#\s*$",
        alt_prompt_terminator: str = r">\s*$",
        username_pattern: str = r"(?:user:|username|login|Applying Interface configuration, please wait ...)",
        pwd_pattern: str = r"assword:",
        delay_factor: float = 1.0,
        max_loops: int = 20,
    ) -> str:
        super().telnet_login(
                pri_prompt_terminator,
                alt_prompt_terminator,
                username_pattern,
                pwd_pattern,
                delay_factor,
                max_loops,
            )