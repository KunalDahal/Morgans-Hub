import threading
import logging
import asyncio
from monitor.run import main as run_monitor_bot
from morgan_c.morgans_c import main as run_editor_bot
from morgan.morgans import main as run_mizu_bot

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
    ]
)
logger = logging.getLogger(__name__)

def run_async_in_thread(async_func, name):
    def wrapper():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            logger.info(f"Starting {name} bot...")
            loop.run_until_complete(async_func())
        except Exception as e:
            logger.error(f"Error in {name} bot: {e}", exc_info=True)
        finally:
            loop.close()
    return wrapper

def main():
    monitor_thread = threading.Thread(
        target=run_async_in_thread(run_monitor_bot, "monitor"),
        daemon=True
    )
    
    editor_thread = threading.Thread(
        target=run_async_in_thread(run_editor_bot, "editor"),
        daemon=True
    )
    
    mizu_thread = threading.Thread(
        target=run_async_in_thread(run_mizu_bot, "mizu"),
        daemon=True
    )

    monitor_thread.start()
    editor_thread.start()
    mizu_thread.start()

    logger.info("All bots started in separate threads")

    try:
        while True:
            if not monitor_thread.is_alive():
                logger.error("Monitor bot thread has died, restarting...")
                monitor_thread = threading.Thread(
                    target=run_async_in_thread(run_monitor_bot, "monitor"),
                    daemon=True
                )
                monitor_thread.start()
                
            if not editor_thread.is_alive():
                logger.error("Editor bot thread has died, restarting...")
                editor_thread = threading.Thread(
                    target=run_async_in_thread(run_editor_bot, "editor"),
                    daemon=True
                )
                editor_thread.start()
                
            if not mizu_thread.is_alive():
                logger.error("Mizu bot thread has died, restarting...")
                mizu_thread = threading.Thread(
                    target=run_async_in_thread(run_mizu_bot, "mizu"),
                    daemon=True
                )
                mizu_thread.start()
                
            threading.Event().wait(5)
            
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt, shutting down...")
    except Exception as e:
        logger.error(f"Unexpected error in main thread: {e}")
    finally:
        logger.info("All bots stopped")

if __name__ == "__main__":
    main()