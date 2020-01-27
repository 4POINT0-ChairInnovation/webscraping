import innovationScraping.utility.configs as Configs
import os
sites_file = Configs.getSiteFile(-1)
print("os")
print(sites_file)
dir = os.path.dirname(sites_file)
print(dir)
with open(sites_file) as sites:
    counter = 0
    index = 0
    file = open(dir + '\\NAICS01P_'+str(counter)+'.txt', 'w')
    for url in sites:
         url = url.strip("\n")
         url = url.strip()
         file.write(url+'\n')
         index = index + 1
         if (index >= 70):
             file.close()
             counter = counter + 1
             file = open(dir + '\\NAICS01P_' + str(counter) + '.txt', 'w')
             index = 0

    file.close()
