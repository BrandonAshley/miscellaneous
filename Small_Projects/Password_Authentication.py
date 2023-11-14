import getpass

database={"GracefulGazer":"OliviaP@ss1",
"ArtisticScribe":"EthanQwerty123",
"MelodicWhisper":"IsabellaPa$$word!2",
"LuckyCharm":"LucasSecur3Pwd",
"SparklingEyes":"SophiaStr0ngPass!",
"DancingFeet":"JacksonP@ss123word",
"SereneJourney":"AvaSafe&Secure1",
"GoldenSmile":"MasonPassw0rd!23",
"EmeraldEyes":"AmeliaP@$$w0rd!5",
"VelvetVoice":"LiamRainyDay7!"}

username= input("Enter username:  ")
password= getpass.getpass("Enter Password")
for i in database.keys():
    if username==i:
        while password != database.get(i):
            password=getpass.getpass("Enter password again:  ")
        break
    
print("Confirmed")

