import downloader as dl

dl.Download("https://music.youtube.com/watch?v=TFYmUz_prtI", "605")

dl.test()

print("Welcome to MedKIT")
input = input("Enter URL:")
dl.list_resolutions(input)