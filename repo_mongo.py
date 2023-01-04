from pymongo import MongoClient
from tabulate import tabulate

client,db,collection = None,None,None

def setup():
    global client
    global db
    global collection
    
    client = MongoClient('localhost',27017)
    db=client['MSD']
    collection = db['songs']

def insert_data(data:dict):
    id = collection.insert_one(data)
    print('Data successfully inserted with id: ', id)


def get_tags():
    
    title = input("Enter a song title: ")
    artist = input("(Optional) Enter an artist: ")
    if artist == '':
        query = {"title" : title}
    else:
        query = {"title" : title, "artist" : artist}

    doc = collection.find(query)
    for x in doc:
        print(tabulate(x['tags'],headers=['Tag','Relevance'], tablefmt="github"))
 
    

def get_songs_with_tag():
    # get user input
    tag = input('Enter a tag: ')
    songs = []
    query = {"tags":{"$elemMatch":{"$elemMatch":{"$eq":tag}}}}
    doc = collection.find(query)
    for x in doc:
        songs.append((x['title'],x['artist']))
    print(tabulate(songs,headers=['Song','Artist'], tablefmt="github"))
        
    

def update_record():
    # get user input
    track_id = input('Enter the track ID of the record you want to update: ')
    field_type = int(input('Enter the field type you want to update: (0) title (1) artist: '))
    new_entry = input('Enter the new value: ')
    f = ''
    match field_type:
        case 0:
            f = 'title'
        case 1:
            f = 'artist'
    query = {'track_id': track_id}
    update = {'$set':{f:new_entry}}
    collection.update_one(query,update)
    doc = collection.find(query)
    for x in doc:
        print(f,(x[f]))
        
def add_tags():
    song = input('Input the track ID of the song you want to add tag/s to: ')
    tags_string = input('Enter the tags and associated relevance factor separated by a semicolon: ')
    tags_list = tags_string.split(';')
    tags = []
    for i in tags_list:
        t = i.split()
        tags.append(t)
    for i in tags:
        collection.update_one({'track_id':song},{'$push':{'tags':i}})
    query = {'track_id': song}
    doc = collection.find(query)
    print('New Tags')
    for x in doc:
        print(tabulate(x['tags'],headers=['New Tags'],tablefmt='github'))
    