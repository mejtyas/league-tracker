import multiprocessing
import time

def process_one():
    import requests
    import json
    import os
    from time import sleep

    def last_match_screenshot():
        from selenium import webdriver
        from webdriver_manager.chrome import ChromeDriverManager
        from selenium.webdriver.chrome.service import Service as ChromeService
        from selenium.webdriver.common.by import By
        from time import sleep
        import requests

        WEBHOOK = 'https://discord.com/api/webhooks/1210589416322760774/BIgVTBvZLl1b2ZBt8FRLdRKhNxbyj0RxDDx-tv60Fr4vn3xIRFGZrSvzk_rENfbjzc3S'

        for i in range(10):    
            try:
                driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
                driver.get(f"https://u.gg/lol/profile/eun1/{GameName}-{GameTag}/overview")

                # bypass cookies visco
                accept_button = driver.find_element(By.XPATH, "//span[contains(text(), 'AGREE')]")
                accept_button.click()

                update_button = driver.find_element(By.XPATH, "//div[contains(text(), 'Update')]")
                update_button.click()

                sleep(9)
                sleep(1)
                myform = driver.find_element(By.CLASS_NAME, "match-history_match-card")
                break
            except Exception:
                print("MINOR FUCKED UP")
                driver.quit()
        myform.screenshot("screenshot.png")
        driver.quit()

        with open("screenshot.png", 'rb') as f:
            files = {
                'file': ("screenshot.png", f, 'image/png')
            }
            requests.post(WEBHOOK, files=files)

    def get_puuid():
        summoner_url = f"https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{GameName}/{GameTag}?api_key={api_key}"
        response = requests.get(summoner_url)
        summoner_data = response.json()
        puuid = summoner_data.get('puuid')
        return puuid

    def get_last_matches():
        puuid = get_puuid() 
        last_matches_url = f"https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count=20&api_key={api_key}"
        response = requests.get(last_matches_url)
        matches = response.json()
        return matches

    def compare_matches():
        puuid = get_puuid() 
        matches = get_last_matches()

        data_to_save = {
            "puuid": puuid,
            "matches": matches
        }

        with open("matchescompare.json", 'w') as json_file:
            json.dump(data_to_save, json_file, indent=4)

        with open('matchescompare.json', 'r') as file:
            compare = file.read()
            
        with open('matches.json', 'r') as file:
            content = file.read()


        if content == compare:
            os.remove('matchescompare.json')
            with open("matches.json", 'w') as json_file:
                json.dump(data_to_save, json_file, indent=4)
        else:
            os.remove('matchescompare.json')
            with open("matches.json", 'w') as json_file:
                json.dump(data_to_save, json_file, indent=4)
            result = True
            return result

    def win_or_lose():
        puuid = get_puuid() 
        matches = get_last_matches()

        data_to_save = {
            "puuid": puuid,
            "matches": matches
        }
        latest_match = data_to_save["matches"][0]
        check_match_url = f"https://europe.api.riotgames.com/lol/match/v5/matches/{latest_match}?api_key={api_key}"
        response = requests.get(check_match_url)
        match = response.json()
        with open('test.json', 'w') as file:
            json.dump(match, file, indent=4)
        win_value = match["info"]["participants"][0]["win"]
        return win_value

    api_key = 'RGAPI-3d31fc6d-d936-46ee-bdca-61ec8024052d'
    GameName = "hrac lolka 5"
    GameTag = "Pepe"

    while(True):
        try:
            result = compare_matches()

            if result == True: # David odehral novej zapas a posle screenshot
                print("New game was found.")
                last_match_screenshot()
                win_value = win_or_lose()
                if win_value == True:
                    print("He won")
                    data = {
                        "content": "specific trigger"
                    }
                    requests.post("https://discord.com/api/webhooks/1210661193753296986/xin41dfYUurd1sLsr6nfn94hrNfFKhIG5IAqpT86PX2-MdTztKp_UHVD1_YmYJvvfhOU", json=data)
                else:
                    print("Dming david")
                    data = {
                        "content": "specific trigger"
                    }
                    requests.post("https://discord.com/api/webhooks/1210661193753296986/xin41dfYUurd1sLsr6nfn94hrNfFKhIG5IAqpT86PX2-MdTztKp_UHVD1_YmYJvvfhOU", json=data)
            else:
                print("No new game found.")
            sleep(4)
        except Exception:
            print("GLOBAL FUCKED UP")

def process_two():
    from discord.ext import commands
    import discord
    import requests
    import json
    import random

    def random_gify():
        # set the apikey and limit
        apikey = "AIzaSyDxUaLQljklQJREtbWVTjCGqNGYmqglKRU"  # click to set to your apikey
        lmt = 10
        ckey = "my_test_app"  # set the client_key for the integration and use the same value for all API calls

        # our test search
        search_term = "loser"

        # get the top 8 GIFs for the search term
        r = requests.get(
            "https://tenor.googleapis.com/v2/search?q=%s&key=%s&client_key=%s&limit=%s" % (search_term, apikey, ckey,  lmt))

        if r.status_code == 200:
            # load the GIFs using the urls for the smaller GIF sizes
            top_8gifs = json.loads(r.content)
            limited_results = top_8gifs['results'][:15]

            # Select a random entry from those limited results
            random_entry = random.choice(limited_results)

            # Extract the nanogif URL from the randomly selected entry
            gif_url = random_entry['media_formats']['gif']['url']
            return gif_url
        else:
            top_8gifs = None

    intents = discord.Intents.all()
    intents.members = True
    bot = commands.Bot(command_prefix='!',intents=intents)

    @bot.event
    async def on_ready():
        print(f'{bot.user.name} has connected to Discord!')

    @bot.event
    async def on_message(message):
        if message.webhook_id:
            if "specific trigger" in message.content:
                user = await bot.fetch_user(383311190971121665)
                gif_url = random_gify()
                print(gif_url)
                await user.send(gif_url)
                file = discord.File('screenshot.png', filename='screenshot.png')    
                await user.send(file=file)

    TOKEN = 'MTIxMDYxMTQ4ODM2OTI3OTAyNg.GDKYt7.N5wmY6womcmxTQqUHmxiYMy5tFNJPFxq2Hz49w'
    bot.run(TOKEN)

if __name__ == '__main__':
    # Create Process objects for each function
    p1 = multiprocessing.Process(target=process_one)
    p2 = multiprocessing.Process(target=process_two)
    
    # Start the processes
    p2.start()
    time.sleep(3)
    p1.start()
    
    # Wait for both processes to finish
    p1.join()
    p2.join()
    
    print("Both processes have finished execution.")