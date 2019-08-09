# discord-bot


## Features

The following is a list of features the bot has:

- [x] generic image upload from folders with auto generated commands
- [x] reboot command
- [ ] reminder function to ping one or more people   
  `!remind "Schnitzel" "datetime" @user1 @user2`
  
- [ ] upload command to create new commands and/or add images to existing ones  
  `!upload <command> <url>`  
  Command should give warning if file is larger than 8 MB.
  

## Commandline Usage

The following arguments are available:

#### -h, --help

  Print arguments, etc.
  
#### -v[vvvv]

Set log level. Maximum is 5.

#### -c, --config <config.json>

Manually set the config that shall be used.

#### --reset

Purge cache before starting.

#### --data <directory>

Local directory for permanent local data.
