import logging

from ..config import *


async def start_battle(ctx, *args):
    if ctx.channel.id == ADMIN_CHANNEL:
        try:
            parsed_args = StudentArenaBot.parse_arguments([*args])
            parsed_args[TOPIC_ACCESSOR] = await self.get_topic_id(ctx)
            logging.info("got it")
        except ValueError:
            logging.info(WRONG_ARGUMENTS_START)
            await self.send_admin(WRONG_ARGUMENTS_START)
            return
        except Exception as e:
            logging.info(f"{e}. Ending start battle")
            return
        logging.info(f"Starting battle with arguments {parsed_args}")
        role = await self.create_arena_role(ctx.guild)
        text_channel = await self.create_battle_channel(ctx.guild, role)
        players = await self.get_players(text_channel, parsed_args[TOPIC_ACCESSOR], SECONDS_TO_JOIN)
        if len(players) == 0:
            # not enough players
            s = f"Stopped battle in {text_channel.name}. No players."
            logging.info(s)
            await self.send_admin(s)
            return
        await self.give_role(players, role)
        new_battle = Quiz(
            text_channel.id,
            ctx.me,
            players,
            self.data_provider.topics[parsed_args[TOPIC_ACCESSOR]],
            DataProvider.get_questions(
                parsed_args[QUESTION_AMOUNT_ACCESSOR], parsed_args[TOPIC_ACCESSOR])
        )
        self.battles[new_battle.cid] = [new_battle, text_channel, role]
        try:
            await self.launch_game(new_battle)
            logging.info(f"Arena in {text_channel.name} has ended.")
            # make all records, ok da?
            if new_battle.state.game_ended:
                logging.info(
                    f"Sending info about session in {text_channel.name} to the backend.")
                self.data_provider.send_session_info(
                    new_battle.dump_game())
        except Exception as e:
            logging.info(
                f"Game {new_battle.cid} stopped by exception {e}.")
            if new_battle.cid in self.battles:
                await self.admin_channel.send(BATTLE_STOPPED_AND_WHY % (text_channel.name, e))
                self.battles[new_battle.cid][0].state.game_in_progress = False
