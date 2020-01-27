from innovationScraping.utility import configs as configs

sitesFile = configs.getSiteFile(-1)

# permanent loop to add "http://" to site name
with open(sitesFile, 'r') as f:
    file_lines = [''.join(['http://', x.strip(), '\n']) for x in f.readlines()]

with open(sitesFile, 'w') as f:
    f.writelines(file_lines)

