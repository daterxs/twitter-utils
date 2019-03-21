import csv
import json
import argparse

parser = argparse.ArgumentParser(description='Procesa los tweets crudos a csv.')
parser.add_argument('--input', type=str, help='Path de los tweets a procesar.')

args = parser.parse_args()

input_file = args.input
out_tweets = 'out_tweets.csv'
out_users = 'out_users.csv'

header_tweets = ['id', 'created_at', 'full_text', 'user_id', 'user_screen_name',
                 'lang', 'is_retweeted', 'retweeted_user_id']
# Otras cosasque se pueden sacar: 'in_reply_to_status_id', 'in_reply_to_user_id',
# 'in_reply_to_screen_name', 'source', 'is_quote_status', 'retweet_count',
# 'favorite_count'
# Mas compicado de sacar (por su estructura): 'entities'

header_users = ['id', 'name', 'screen_name', 'location', 'description', 'statuses_count',
                'favourites_count', 'followers_count', 'friends_count', 'created_at',
                'lang', 'default_profile', 'default_profile_image']
# Otras cosas que se pueden sacar: 'url', 'listed_count', 'verified'

def extract_tweet_info(status):
    """Extrae la info del tweet como dict. """

    # Si es un RT no pongo el texto y luego proceso el RT
    # Ya que el RT tiene el mismo texto (pero me lo da truncado)
    if 'retweeted_status' in status:
        is_retweeted = True
        retweeted_user_id = status['retweeted_status']['id']
        full_text = ''
    else:
        is_retweeted = False
        retweeted_user_id = ''
        # Miro que key tiene ('full_text' o 'text')
        if not 'extended_tweet' in status:
            if 'full_text' in status:
                full_text = status['full_text']
            else:
                full_text = status['text']
        # Si tiene 'extended_tweet' siempre agarro el texto completo
        else:
            full_text = status['extended_tweet']['full_text']

    out = [status['id'], status['created_at'], full_text, status['user']['id'],
           status['user']['screen_name'], status['lang'], is_retweeted, retweeted_user_id ]

    return out

def extract_user_info(user):
    """Extrae la info del usuario como dict"""

    out = [user[k] for k in header_users]
    return out

if __name__ == '__main__':

    uniques_tweet_id = set()
    uniques_user_id = set()

    with open(input_file, 'r') as file_in, \
         open(out_tweets, 'w') as file_tweets,\
         open(out_users, 'w') as file_users:

        tweets_writer = csv.writer(file_tweets)
        users_writer = csv.writer(file_users)

        tweets_writer.writerow(header_tweets)
        users_writer.writerow(header_users)

        for i, line in enumerate(file_in):
            if i % 10000 == 0:
                print('\rProcesando la linea: {}'.format(i), end='')

            status = json.loads(line)

            if status['id'] not in uniques_tweet_id:
                tweets_writer.writerow(extract_tweet_info(status))
                uniques_tweet_id.add(status['id'])

            if status['user']['id'] not in uniques_user_id:
                users_writer.writerow(extract_user_info(status['user']))
                uniques_user_id.add(status['user']['id'])

            if 'retweeted_status' in status:
                if status['retweeted_status']['id'] not in uniques_tweet_id:
                    tweets_writer.writerow(extract_tweet_info(status['retweeted_status']))
                    uniques_tweet_id.add(status['retweeted_status']['id'])
                if status['retweeted_status']['user']['id'] not in uniques_user_id:
                    users_writer.writerow(extract_user_info(status['retweeted_status']['user']))
                    uniques_user_id.add(status['retweeted_status']['user']['id'])
