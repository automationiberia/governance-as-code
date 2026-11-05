#!/bin/sh
# Same starting state for the original and the modernized role.
set -e
groupadd -g 1300 oldgroup
useradd olduser
useradd -f 30 -u 1220 orainfra   # existing user with a 30-day inactivity period
