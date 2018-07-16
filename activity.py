
def get_minable(tough):
    mineables = ["stone", "coal", "copper", "iron", "tin", "diamond"]
    return mineables[:tough//50]