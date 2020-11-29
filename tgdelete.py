#!/bin/env python3
from telethon.sync import TelegramClient, events
from telethon import functions, types
import argparse
import asyncio

client = TelegramClient("telegram-deleter", "425874", "d2f7f845f91154f283e313ebb76245a2")

async def delete_chat(chatid, timer = 5):
	# Fetch the chat from the ID
	chat = await client.get_entity(chatid)

	# It's more efficient on both speed and network usage
	# , if I give the delete function a list of IDs
	# instead of going one at a time.
	messageids = list()

	# Start iterating over the messages.
	print(f"!!!! GATHERING ALL SELF MESSAGES FROM CHAT {chat.title} !!!!", flush = True)
	async for message in client.iter_messages(chat, from_user = "me"):
		print(f"[{chat.title}] {message.text}")
		messageids.append(message.id)

	if timer:
		print(f"!!!! DELETING MESSAGES in {timer} seconds! !!!!")
		await asyncio.sleep(timer)
	await client.delete_messages(chat, messageids, revoke = True)

	print(f"{len(messageids)} messages deleted!")

async def dump_chats():
	async for chat in client.iter_dialogs():
		if chat.name:
			print(f"{chat.name} {chat.id}")
		else:
			print(f"[NO NAME] {chat.id}")

async def count_messages():
	# TODO: make faster
	counts = {}

	async for chat in client.iter_dialogs():
		print(f"Counting messages in {chat.name}...")
		counts.update({chat.name: 0})
		async for message in client.iter_messages(chat, from_user = "me"):
			counts[chat.name]+=1

	print(counts)

async def delete_chats(exclude = list()):
	print("!!!! DELETING MESSAGES FROM ALL PUBLIC CHAT ROOMS !!!!")
	async for chat in client.iter_dialogs():
		if not chat.is_group:
			print("Skipping non-group thread...")
			continue

		if chat.id in exclude:
			print(f"Skipping {chat.name} due to user request...")
			continue

		await delete_chat(chat.id, timer = 2)

async def timer_delete(event):
	print(f"New message {event.message.id} in chat {event.message.peer_id}")
	print("Waiting 600 second(s) for secret termination...")
	await asyncio.sleep(600)
	await event.message.delete()

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--delete-chat-id", type = int)
	parser.add_argument("--delete-public-chats", action = "store_true")
	parser.add_argument("--global-delete-exclude", type = int, nargs = "*", default = [])
	parser.add_argument("--dump-chats", action = "store_true")
	parser.add_argument("--count-messages", action = "store_true")
	parser.add_argument("--timer-delete", action = "store_true")
	args = parser.parse_args()

	with client:
		if args.timer_delete:
			client.add_event_handler(timer_delete, events.NewMessage(from_users = "me"))
			client.run_until_disconnected()
			exit(0)

		if args.dump_chats:
			client.loop.run_until_complete(dump_chats())
			exit(0)

		if args.count_messages:
			client.loop.run_until_complete(count_messages())
			exit(0)

		if args.delete_public_chats:
			client.loop.run_until_complete(delete_chats(args.global_delete_exclude))
			exit(0)

		if not args.delete_chat_id:
			raise Exception("Must have chat to delete from!")

		client.loop.run_until_complete(delete_chat(args.delete_chat_id))
