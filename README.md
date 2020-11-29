# telegram-deleter
A mass message deleter for Telegram.

## How to use

### List Chats
```
$ ./tgdelete.py --dump-chats
...
deletion testing -456873081
...
```

The output of the chat output is the chat name first followed by the chat ID,
which is used in the following commands.

### Delete a single chat
```
$ ./tgdelete.py --delete-chat-id -456873081
!!!! GATHERING ALL SELF MESSAGES FROM CHAT deletion testing !!!!
[deletion testing] 45
...
!!!! DELETING MESSAGES in 5 seconds! !!!!
6 messages deleted!
```

TGDelete prints out the messages as it is fetching them for deletion which is what the "45" is.

### Delete ALL chats
This is the nuclear option that erases ALL messages sent by you in any groups you are in.
It does NOT affect channels or private message threads.

```
$ ./tgdelete.py --delete-public-chats
!!!! DELETING MESSAGES FROM ALL PUBLIC CHAT ROOMS !!!!
!!!! GATHERING ALL SELF MESSAGES FROM CHAT deletion testing !!!!
!!!! DELETING MESSAGES in 2 seconds! !!!!
```

The reason there were no messages printed was because there were no messages in the listed group.

### Delete ALL chats but xyz

```
$ ./tgdelete.py --delete-public-chats --global-delete-exclude -456873081
!!!! DELETING MESSAGES FROM ALL PUBLIC CHAT ROOMS !!!!
!!!! GATHERING ALL SELF MESSAGES FROM CHAT Trackers - all things torrent !!!!
!!!! DELETING MESSAGES in 2 seconds! !!!!
Skipping deletion testing due to user request...
```

This does the same thing as above but excludes one or more groups from the
mass deletion.

You can specify more than more ID to exclude by putting them one
after the other separated by spaces like this, 
`--global-delete-exclude -456873081 -457586326`.

### Timer Deletion
```
$ ./tgdelete.py --timer-delete
New message 98765 in chat PeerChannel(channel_id=123456)
Waiting 120 second(s) for secret termination...
```

Timer deletion is pretty self explanatory.

After every message sent there is a 120 second timer placed on the message, after this timer expires the message is deleted.
