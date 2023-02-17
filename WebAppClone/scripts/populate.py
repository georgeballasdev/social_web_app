def run():
    from django.contrib.auth.hashers import make_password
    from django.contrib.auth.models import User
    from feed.models import Post, Comment
    from groups.models import Group
    from notifications.models import Client
    from random import randint, choice, sample
    from users.models import Profile


    NUMBER_OF_POSTS = 100
    NUMBER_OF_GROUPS = 40
    MAX_NUMBER_OF_COMMENTS = 10
    MAX_NUMBER_OF_GROUPS_TO_JOIN = 3

    def get_random_sentence():
        return sentences[randint(0, sentences_n-1)]

    def get_random_title():
        return titles[randint(0, titles_n-1)]

    def get_random_image():
        i = randint(0, 99)
        return f'sample-images/{i}.jpg'

    def create_user(name):
        user = User.objects.create(
                username=name,
                email=f'{name}@socialbook.com',
                password=make_password('Complex111!')
        )

        Profile.objects.create(
                user=user,
                bio=get_random_sentence(),
                pic=get_random_image(),
        )

        Client.objects.create(
                user=user,
                notifications_channel='a',
                status_channel='a'
        )
        return user

    def add_friends(user, new_friends):
        for friend in new_friends:
            user.profile.friends.add(friend)
            friend.profile.friends.add(user)

    def make_friendships(users):
        for i, user in enumerate(users[:-1]):
            new_friends = sample(users[i+1:], randint(1, len(users[i+1:])))
            add_friends(user, new_friends)

    def create_group(user):
        if choice((True, False)):
            Group.objects.create(
                owner=user,
                title=get_random_title(),
                info=get_random_sentence(),
                img=get_random_image()
                )
        else:
            Group.objects.create(
                owner=user,
                title=get_random_title(),
                info =get_random_sentence()
        )

    def join_groups(user):
        for _ in range(randint(1, MAX_NUMBER_OF_GROUPS_TO_JOIN)):
            group = user.profile.get_random_group()
            if group == None:
                return
            group.members.add(user)
            user.profile.groups.add(group)

    def create_post(user):
        post = Post.objects.create(
                owner=user,
                text =get_random_sentence()
                )
        if choice((True, False)):
            post.img = get_random_image()
            post.save()
        if choice((True, False)):
            post.of_group = choice(post.owner.profile.groups.all())
            post.save()

        owner_friends = post.owner.profile.friends.all()
        for friend in owner_friends:
            if choice((True, False)):
                post.liked_by.add(friend)

        for _ in range(randint(0, MAX_NUMBER_OF_COMMENTS)):
            Comment.objects.create(
                of_post=post,
                owner=choice(owner_friends),
                text=get_random_sentence()
            )

    print('STARTING PROCESS...')

    with open('scripts/names.txt') as file:
        names = file.readlines()
    print('LOADED NAMES...')

    with open('scripts/random_sentences.txt') as file:
        sentences = file.readlines()
    sentences_n = len(sentences)
    print('LOADED SENTENCES...')

    with open('scripts/random_phrases.txt') as file:
        titles = file.readlines()
    titles_n = len(titles)
    print('LOADED TITLES...')

    users = []
    for name in names:
        user = create_user(name.strip())
        users.append(user)
    print('USERS CREATED...')

    make_friendships(users)
    print('FRIENDSHIPS CREATED...')

    for _ in range(NUMBER_OF_GROUPS):
        create_group(choice(users))
    print('GROUPS CREATED...')

    for user in users:
        join_groups(user)
    print('GROUPS JOINED...')

    for _ in range(NUMBER_OF_POSTS):
        create_post(choice(users))
    print('POSTS CREATED...')

    print('POPULATING COMPLETED.')