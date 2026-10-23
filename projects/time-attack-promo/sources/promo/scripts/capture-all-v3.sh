#!/bin/sh
# Re-captures every source of Film A against current develop (new race HUD), 2026-10-23.
P=/home/farrell/Videos/OGGF/ta-promo-a
S=$P/scripts/run-promo-v3.sh
R=$P/route/ghz1.route
$S lobby-s3k-profile lobby s3k profile; echo "lobby-s3k-profile $?"
$S lobby-s1 lobby s1; echo "lobby-s1 $?"
$S lobby-s2 lobby s2; echo "lobby-s2 $?"
$S names-relay namesrelay $R; echo "names-relay $?"
$S race-clean3 race $R 75 clean intl 9; echo "race-clean3 $?"
$S race-death race $R 120 death intl 9; echo "race-death $?"
$S race-256 race $R 75 clean bots 256; echo "race-256 $?"
