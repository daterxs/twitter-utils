# twitter-utils

Script para procesar tweets.

### raw2csv.py

Separa el crudo en dos csv sin duplicados. Uno de  usuarios con las columnas:

- id: id del usuario.
- name: nombre del usuario.
- screen_name: screen_name (arroba) del usuario.
- location: location del usuario.
- description: descripcion del usuario.
- statuses_count: cantidad de tweets del usuario.
- favourites_count: cantidad de favoritos.
- followers_count: cantidad de seguidores.
- friends_count: cantidad de gente que el usuario seguir.
- created_at: fecha de creacion de la cuenta.
- lang: lenguaje de la cuenta.
- default_profile: si no cambio la configuracion del usuario (como la foto de fondo).
- default_profile_image: si no cambio el avatar.

y otro con los tweets con las columnas:

- id: id del tweet.
- created_at: fecha de creacion.
- full_text: texto completo del tweet. Si es un RT, full_text esta vacio y el correspondiente texto esta en el tweet con el id 'rt_id'.
- user_id: id del usuario que hace el tweet.
- user_screen_name: screen_name (arroba) del usuario que hace el tweet.
- lang: lenguaje del tweet.
- is_retweeted: 'True' si es un retweet.
- rt_id: id del tweet original. Si es un retweet el texto esta en ese id.

Necesita python3.

Uso:

`python3 raw2csv.py --input path_to_input`
