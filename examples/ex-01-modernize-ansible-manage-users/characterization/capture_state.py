"""Capture the account state the role is responsible for, as JSON.

Runs on the managed host (Python 3.9 in UBI 9, where the crypt module exists).
The password hash itself is not recorded, only whether it equals the user name.
"""
import crypt
import grp
import json
import pwd
import spwd
import sys

USERS = ["oracle", "orainfra", "olduser"]
GROUPS = ["oinstall", "dba", "oldgroup"]
state = {"users": {}, "groups": {}}
for name in USERS:
    try:
        p = pwd.getpwnam(name)
    except KeyError:
        state["users"][name] = "absent"
        continue
    s = spwd.getspnam(name)
    state["users"][name] = {
        "uid": p.pw_uid,
        "gid": p.pw_gid,
        "comment": p.pw_gecos,
        "home": p.pw_dir,
        "shell": p.pw_shell,
        "groups": sorted(g.gr_name for g in grp.getgrall() if name in g.gr_mem),
        "last_change": s.sp_lstchg,
        "min": s.sp_min,
        "max": s.sp_max,
        "inactive": s.sp_inact,
        "expire": s.sp_expire,
        "password_equals_username": s.sp_pwdp.startswith("$") and crypt.crypt(name, s.sp_pwdp) == s.sp_pwdp,
    }
for name in GROUPS:
    try:
        state["groups"][name] = grp.getgrnam(name).gr_gid
    except KeyError:
        state["groups"][name] = "absent"
json.dump(state, sys.stdout, indent=2, sort_keys=True)
