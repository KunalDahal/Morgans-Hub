import asyncio
import logging
from monitor.huh import ChannelMonitor
from monitor.sync import sync_channel_files
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
    ]
)

async def main():
   
    monitor = ChannelMonitor()
    
    monitor_task = asyncio.create_task(monitor.run())
    sync_task = asyncio.create_task(sync_channel_files())
    
    await asyncio.gather(monitor_task, sync_task)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Bot stopped by user")
    except Exception as e:
        logging.error(f"Fatal error: {e}")