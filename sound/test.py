import queryer

# Play sequentially car (Volume 3) then door (Volume 5)
print(
    queryer.playsounds({
        'truck': 3,
        'door': 5
    }, 1, False)
)

# Play overlay 4 Cats at Volume 8
print(
    queryer.playsounds({
        'cat': 8
    }, 4, True)
)
