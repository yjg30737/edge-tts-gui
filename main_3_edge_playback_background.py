import asyncio

async def speech(text, voice) -> None:
    process = await asyncio.create_subprocess_exec(
        "edge-playback",
        f"--voice={voice}",
        f"--text={text}",
    )
    await process.wait()  # 비동기적으로 프로세스를 기다림

if __name__ == "__main__":
    TEXT = 'Hello World! How are you guys doing? I hope great, cause I am having fun and honestly it has been a blast'
    VOICE = "en-US-AndrewMultilingualNeural"
    asyncio.run(speech(TEXT, VOICE))
    print('abc')
