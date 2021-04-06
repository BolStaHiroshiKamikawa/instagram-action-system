import datetime
from time import sleep
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import configparser
import psycopg2
from psycopg2.extras import DictCursor
import os
import requests
import random
from dateutil.relativedelta import relativedelta

config = configparser.ConfigParser()
config.read('../config.ini')

class WebDriver :

    def __init__(self) :
        self.options = webdriver.ChromeOptions()
        self.options.add_argument(r'--user-data-dir=C:\Users\MT4ver2-g23-cHLCokI8\AppData\Local\Google\Chrome\User Data')
        self.options.add_argument('--profile-directory=Profile 1')
        # self.options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=self.options)
        self.driver.implicitly_wait(10)
        self.wait = WebDriverWait(self.driver, 5)

    def access(self, url) :
        sleep(int(config['PROGRAM']['ACCESS_SLEEP']))
        self.driver.get(url)
        self.wait.until(EC.presence_of_all_elements_located)

    def quit(self) :
        sleep(int(config['PROGRAM']['ACCESS_SLEEP']))
        self.driver.quit()

    def input(self, xpath, key) :
        sleep(int(config['PROGRAM']['ACCESS_SLEEP']))
        self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
        self.driver.find_element_by_xpath(xpath).send_keys(key)

    def click(self, xpath) :
        sleep(int(config['PROGRAM']['ACCESS_SLEEP']))
        self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
        self.driver.find_element_by_xpath(xpath).click()

    def text(self, xpath) :
        try :
            sleep(int(config['PROGRAM']['ACCESS_SLEEP']))
            self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
        except :
            return None
        return self.driver.find_element_by_xpath(xpath).text

    def check(self, xpath, text1=None, text2=None, text3=None) :
        sleep(int(config['PROGRAM']['ACCESS_SLEEP']))
        self.wait.until(EC.presence_of_all_elements_located)
        if text3 :
            try :
                if self.driver.find_element_by_xpath(xpath).text == text1 or self.driver.find_element_by_xpath(xpath).text == text2 or self.driver.find_element_by_xpath(xpath).text == text3 :
                    return True
                return False
            except :
                return None
        elif text2 :
            try :
                if self.driver.find_element_by_xpath(xpath).text == text1 or self.driver.find_element_by_xpath(xpath).text == text2 :
                    return True
                return False
            except :
                return None
        elif text1 :
            try :
                if self.driver.find_element_by_xpath(xpath).text == text1 :
                    return True
                return False
            except :
                return None
        else :
            try :
                self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
                self.driver.find_element_by_xpath(xpath)
                return True
            except :
                return None

    def waiting(self, xpath) :
        self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))

class DataAccess :

    def __init__(self, table, where1=None, key1=None, where2=None, key2=None, where3=None, key3=None) :

        connection = psycopg2.connect(
            f"dbname={os.environ['PSQL_DBNAME']} host={os.environ['PSQL_HOST']} user={os.environ['PSQL_USER']} password={os.environ['PSQL_PASSWORD']} sslmode={config['POSTGRESQL']['SSLMODE']}"
        )

        cur = connection.cursor(cursor_factory=DictCursor)
        if where3 and key3 :
            cur.execute(f"select * from {table} where {where1}='{key1}' and {where2}='{key2}' and {where3}='{key3}';")
        elif where2 and key2 :
            cur.execute(f"select * from {table} where {where1}='{key1}' and {where2}='{key2}';")
        elif where1 and key1 :
            cur.execute(f"select * from {table} where {where1}='{key1}';")
        else :
            cur.execute(f"select * from {table};")
        self.list = cur.fetchall()

        connection.close()

    def makelist(self, key) :
        data = []
        for row in self.list :
            data.append(row[key])
        return data

    def makelist_range() :
        data = []
        for row in self.list :
            pass
        return

def login(web, account) :
    web.access(config['SET']['URL'])
    web.input(config['XPATH']['LOGIN_NAME_BOX'], account['username'])
    web.input(config['XPATH']['LOGIN_PASSWORD_BOX'], account['password'])
    web.click(config['XPATH']['LOGIN_BTN'])
    sleep(5)
    web.access(config['SET']['URL'])

def logout(web) :
    web.access(config['SET']['URL'])
    web.click(config['XPATH']['PROFILE_BTN'])
    web.click(config['XPATH']['LOGOUT_BTN'])

def firstdaySet(user) :
    if user['plan_id'] == 1 :
        connection = psycopg2.connect(
            f"dbname={os.environ['PSQL_DBNAME']} host={os.environ['PSQL_HOST']} user={os.environ['PSQL_USER']} password={os.environ['PSQL_PASSWORD']} sslmode={config['POSTGRESQL']['SSLMODE']}"
        )
        cur = connection.cursor(cursor_factory=DictCursor)

        time_now = datetime.datetime.now()
        cur.execute(f"update main_users set trial_start = '{time_now}' where id = '{user['id']}';")

        connection.commit()
        connection.close()

    else :
        connection = psycopg2.connect(
            f"dbname={os.environ['PSQL_DBNAME']} host={os.environ['PSQL_HOST']} user={os.environ['PSQL_USER']} password={os.environ['PSQL_PASSWORD']} sslmode={config['POSTGRESQL']['SSLMODE']}"
        )
        cur = connection.cursor(cursor_factory=DictCursor)

        time_now = datetime.datetime.now()
        cur.execute(f"update main_users set running_start = '{time_now}' where id = '{user['id']}';")

        connection.commit()
        connection.close()

def hashtagAction(web, user) :
    hashtags = DataAccess('main_hashtags', 'user_id', user['id'])
    counter = 0
    print('アクション：ハッシュタグアクション')

    if len(hashtags.list) < user['hashtag_number'] :
        hashtag = hashtags.list[0]['name']
        connection = psycopg2.connect(
            f"dbname={os.environ['PSQL_DBNAME']} host={os.environ['PSQL_HOST']} user={os.environ['PSQL_USER']} password={os.environ['PSQL_PASSWORD']} sslmode={config['POSTGRESQL']['SSLMODE']}"
        )
        cur = connection.cursor(cursor_factory=DictCursor)

        time_now = datetime.datetime.now()
        cur.execute(f"update main_users set hashtag_number = '2' where id = '{user['id']}';")

        connection.commit()
    else :
        hashtag = hashtags.list[user['hashtag_number'] - 1]['name']
        connection = psycopg2.connect(
            f"dbname={os.environ['PSQL_DBNAME']} host={os.environ['PSQL_HOST']} user={os.environ['PSQL_USER']} password={os.environ['PSQL_PASSWORD']} sslmode={config['POSTGRESQL']['SSLMODE']}"
        )
        cur = connection.cursor(cursor_factory=DictCursor)

        time_now = datetime.datetime.now()
        cur.execute(f"update main_users set hashtag_number = '{user['hashtag_number'] + 1}' where id = '{user['id']}';")

        connection.commit()

    web.access(config['SET']['HASHTAG_URL'] + hashtag)
    web.click(config['XPATH']['HASH_NEW_POST_BTN'])
    print(f'ハッシュタグ名：{hashtag}')

    for i in range(10) :
        try :
            post_username = web.text(config['XPATH']['HASH_POST_USERNAME'])
            print(f'投稿者：{post_username}')

            time_now = datetime.datetime.now()
            cur.execute(f"insert into main_subcompetitors (user_id, username, finished, created_at, updated_at) values ({user['id']}, '{post_username}', 'False', '{time_now}', '{time_now}');")

            connection.commit()

            web.click(config['XPATH']['HASH_POST_LIKE_BTN'])
            web.click(config['XPATH']['HASH_POST_LIKED_ACCOUNT_BTN'])

            limit = range(random.randint(2, 4))
            i = 1
            while True :
                notfollowed = web.check(f'/html/body/div[6]/div/div/div[2]/div/div/div[{i}]/div[3]/button', 'フォローする')

                if notfollowed == False:
                    continue
                elif notfollowed == None :
                    break

                username = web.text(f'/html/body/div[6]/div/div/div[2]/div/div/div[{i}]/div[2]/div[1]/div/span/a')

                web.click(f'/html/body/div[6]/div/div/div[2]/div/div/div[{i}]/div[3]/button')
                i += 1
                counter += 1
                sleep(int(config['PROGRAM']['ACTION_SLEEP']))

            web.click(config['XPATH']['HASH_POST_LIKED_ACCOUNT_BACK_BTN'])
            web.click(config['XPATH']['HASH_POST_NEXT_BTN'])
        except :
            web.click(config['XPATH']['HASH_POST_NEXT_BTN'])

    cur.execute(f"update main_users set counter = '{user['counter'] + 1}' where id = '{user['id']}';")
    connection.commit()
    connection.close()
    print(f'フォロー：{counter}アカウント')

def competitorAction(web, user) :
    competitors = DataAccess('main_competitors', 'user_id', user['id'])
    subcompetitors = DataAccess('main_subcompetitors', 'user_id', user['id'], 'finished', 'False')
    counter = 0
    print('アクション：競合アクション')

    if len(competitors.list) < user['competitor_number'] :
        competitor = competitors.list[0]['name']
        connection = psycopg2.connect(
            f"dbname={os.environ['PSQL_DBNAME']} host={os.environ['PSQL_HOST']} user={os.environ['PSQL_USER']} password={os.environ['PSQL_PASSWORD']} sslmode={config['POSTGRESQL']['SSLMODE']}"
        )
        cur = connection.cursor(cursor_factory=DictCursor)

        time_now = datetime.datetime.now()
        cur.execute(f"update main_users set competitor_number = '2' where id = '{user['id']}';")

        connection.commit()
    else :
        competitor = competitors.list[user['competitor_number'] - 1]['username']
        connection = psycopg2.connect(
            f"dbname={os.environ['PSQL_DBNAME']} host={os.environ['PSQL_HOST']} user={os.environ['PSQL_USER']} password={os.environ['PSQL_PASSWORD']} sslmode={config['POSTGRESQL']['SSLMODE']}"
        )
        cur = connection.cursor(cursor_factory=DictCursor)

        time_now = datetime.datetime.now()
        cur.execute(f"update main_users set competitor_number = '{user['competitor_number'] + 1}' where id = '{user['id']}';")

        connection.commit()

    web.access(config['SET']['URL'] + competitor)
    web.click(config['XPATH']['PROFILE_FOLLOWER_BUTTON'])

    limit = random.randint(2, 4)
    i = 1
    while i <= limit :
        try :
            notfollowed = web.check(f'/html/body/div[5]/div/div/div[2]/ul/div/li[{i}]/div/div[3]/button', 'フォローする')

            if notfollowed == False:
                i+=1
                continue
            elif notfollowed == None :
                break

            username = web.text(f'/html/body/div[5]/div/div/div[2]/ul/div/li[{i}]/div/div[2]/div[1]/div/div/span/a')
            print(username)

            web.click(f'/html/body/div[5]/div/div/div[2]/ul/div/li[{i}]/div/div[3]/button')
            counter += 1
            i+=1
            sleep(int(config['PROGRAM']['ACTION_SLEEP']))
        except :
            print('Error: アクションエラー')
            break

    web.click(config['XPATH']['PROFILE_FOLLOWER_BACK_BTN'])
    web.click(config['XPATH']['PROFILE_NEW_POST_BTN'])

    while True :
        try :
            if not web.check(config['XPATH']['PROFILE_POST_LIKED_ACCOUNT_BTN']) :
                web.click(config['XPATH']['PROFILE_POST_NEXT_BTN'])

            web.click(config['XPATH']['PROFILE_POST_LIKED_ACCOUNT_BTN'])
            for i in range(random.randint(2, 4)) :
                notfollowed = web.check(f'/html/body/div[6]/div/div/div[2]/div/div/div[{i}]/div[3]/button', 'フォローする')

                if not notfollowed :
                    continue

                username = web.text(f'/html/body/div[6]/div/div/div[2]/div/div/div[{i}]/div[2]/div[1]/div/span/a')

                web.click(f'/html/body/div[6]/div/div/div[2]/div/div/div[{i}]/div[3]/button')
                counter += 1

                sleep(int(config['PROGRAM']['ACTION_SLEEP']))
        except :
            print('Error: アクションエラー')
        break

    connection = psycopg2.connect(
        f"dbname={os.environ['PSQL_DBNAME']} host={os.environ['PSQL_HOST']} user={os.environ['PSQL_USER']} password={os.environ['PSQL_PASSWORD']} sslmode={config['POSTGRESQL']['SSLMODE']}"
    )
    cur = connection.cursor(cursor_factory=DictCursor)

    for subcompetitor in subcompetitors.list :
        try :
            web.access(config['SET']['URL'] + subcompetitor['username'])
            web.click(config['XPATH']['PROFILE_FOLLOWER_BUTTON'])

            limit = random.randint(2, 4)
            i = 1
            while i < limit :
                notfollowed = web.check(f'/html/body/div[5]/div/div/div[2]/ul/div/li[{i}]/div/div[3]/button', 'フォローする')

                if notfollowed == False:
                    i+=1
                    continue
                elif notfollowed == None :
                    break

                username = web.text(f'/html/body/div[5]/div/div/div[2]/ul/div/li[{i}]/div/div[2]/div[1]/div/div/span/a')

                web.click(f'/html/body/div[5]/div/div/div[2]/ul/div/li[{i}]/div/div[3]/button')
                counter += 1
                i+=1
                sleep(int(config['PROGRAM']['ACTION_SLEEP']))
        except :
            print('Error: アクションエラー')

        time_now = datetime.datetime.now()
        cur.execute(f"update main_subcompetitors set finished = 'True' where id = '{subcompetitor['id']}';")

        connection.commit()

    cur.execute(f"update main_users set counter = '{user['counter'] + 1}' where id = '{user['id']}';")
    connection.commit()
    connection.close()

    print(f'フォロー：{counter}アカウント')

def updateStatus(user) :
    time_now = datetime.datetime.now().replace(tzinfo=datetime.timezone.utc)
    if user['plan_id'] == 1 :
        finish_time = user['trial_start'] + datetime.timedelta(day = 7)
        if time_now > finish_time :
            print('体験終了')
            connection = psycopg2.connect(
                f"dbname={os.environ['PSQL_DBNAME']} host={os.environ['PSQL_HOST']} user={os.environ['PSQL_USER']} password={os.environ['PSQL_PASSWORD']} sslmode={config['POSTGRESQL']['SSLMODE']}"
            )
            cur = connection.cursor(cursor_factory=DictCursor)
            cur.execute(f"update main_users set status_id = 5 where id = '{user['id']}';")

            connection.commit()
            connection.close()
    elif user['plan_id'] == 2 :
        finish_time = user['running_start'] + relativedelta(months = 1)
        if time_now > finish_time :
            print('体験終了')
            connection = psycopg2.connect(
                f"dbname={os.environ['PSQL_DBNAME']} host={os.environ['PSQL_HOST']} user={os.environ['PSQL_USER']} password={os.environ['PSQL_PASSWORD']} sslmode={config['POSTGRESQL']['SSLMODE']}"
            )
            cur = connection.cursor(cursor_factory=DictCursor)
            cur.execute(f"update main_users set status_id = 5 where id = '{user['id']}';")

            connection.commit()
            connection.close()
    elif user['plan_id'] == 3 :
        finish_time = user['running_start'] + relativedelta(months = 3)
        if time_now > finish_time :
            print('体験終了')
            connection = psycopg2.connect(
                f"dbname={os.environ['PSQL_DBNAME']} host={os.environ['PSQL_HOST']} user={os.environ['PSQL_USER']} password={os.environ['PSQL_PASSWORD']} sslmode={config['POSTGRESQL']['SSLMODE']}"
            )
            cur = connection.cursor(cursor_factory=DictCursor)
            cur.execute(f"update main_users set status_id = 5 where id = '{user['id']}';")

            connection.commit()
            connection.close()
    elif user['plan_id'] == 4 :
        finish_time = user['running_start'] + relativedelta(months = 6)
        if time_now > finish_time :
            print('体験終了')
            connection = psycopg2.connect(
                f"dbname={os.environ['PSQL_DBNAME']} host={os.environ['PSQL_HOST']} user={os.environ['PSQL_USER']} password={os.environ['PSQL_PASSWORD']} sslmode={config['POSTGRESQL']['SSLMODE']}"
            )
            cur = connection.cursor(cursor_factory=DictCursor)
            cur.execute(f"update main_users set status_id = 5 where id = '{user['id']}';")

            connection.commit()
            connection.close()

def main(action_time_set = 'TEST') :
    print('Start ' + action_time_set + ' session.')

    users = DataAccess('main_users')

    web = WebDriver()

    for user in users.list :
        if user['status_id'] == 1 or user['status_id'] == 4 or user['status_id'] == 5 :
            continue

        print('---------------------------')
        print(f"username: {user['username']}")
        if user['counter'] == 1 :
            print('Today is the first day.')
            firstdaySet(user)

        try :
            login(web, user)
            web.waiting(config['XPATH']['PROFILE_BTN'])
        except :
            import traceback
            traceback.print_exc()
            print('Error: ログインできませんでした。')
            continue

        if user['counter'] % 2 == 0 :
            print('competitor action')
            try :
                competitorAction(web, user)
            except :
                print('Error: 競合アクション中にエラーが発生しました。ログアウトします。')
                updateStatus(user)
                logout(web)
                continue
        else :
            print('Action: hashtag action')
            try :
                hashtagAction(web, user)
            except :
                print('Error: ハッシュタグアクション中にエラーが発生しました。ログアウトします。')
                updateStatus(user)
                logout(web)
                continue

        updateStatus(user)

        logout(web)

    web.quit()

if __name__ == '__main__' :
    main()
