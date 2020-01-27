street_no_pat = "\d+[A-zàâäôéèëêïîçùûüÿæœÀÂÄÔÉÈËÊÏÎŸÇÙÛÜÆŒ]?(\s|,|,\s)[A-zàâäôéèëêïîçùûüÿæœÀÂÄÔÉÈËÊÏÎŸÇÙÛÜÆŒ]+"
postal_code_pat = "[ABCEGHJKLMNPRSTVXY][0-9][ABCEGHJKLMNPRSTVWXYZ]\s?[0-9][ABCEGHJKLMNPRSTVWXYZ][0-9]"
province_pat = "(AB|ALB|Alta|alberta|BC|CB|British Columbia|LB|Labrador|MB|Man|Manitoba|N[BLTSU]|Nfld|NF|Newfoundland|NWT|Northwest Territories|Nova Scotia|New Brunswick|Nunavut|ON|ONT|Ontario|PE|PEI|IPE|Prince Edward Island|QC|PC|QUE|QU|Quebec|Québec|SK|Sask|Saskatchewan|YT|Yukon|Yukon Territories)"
city_pat = "([A-Z][a-z.-]+\s?)+"
middle_pat= "(\s|,|,\s)"
real_title_words = ['Talent', 'Designer', 'EVP,', 'Chairman', 'Senior', 'Systems', 'Principal', 'Admin',
                         'Finance,', 'Founder,',
                         'Technology', 'Officer', 'Accountant', 'Permits,', 'Administrative', 'Architect', 'Counsel,',
                         'Board', 'Member', 'SVP,Legal', 'Scientist', 'Consultant', 'Vice', 'Co-CEO', 'Investment',
                         'Medical',
                         'Development', 'Treasurer,', 'Compliance,', 'Marketing', 'Treasurer', 'CIO', 'Office',
                         'Manager,', 'Corporate',
                         'Executive', 'General', 'Operating', 'Engineering', 'Partner', 'Research', 'Human', 'Founding',
                         'Investor',
                         'Administration', 'President', 'Director', 'Business', 'Creative', 'Co-Chief', 'Sales',
                         'Development,', 'Secretary',
                         'Associate', 'Relations', 'Manager', 'Chairman,', 'VP,', 'Venture', 'CEO', 'Co-founder',
                         'Accounting', 'Counsel', 'Co-President', 'CFO,', 'Resources', 'President,', 'Product',
                         'CTO,COO', 'Secretary,',
                         'CFO', 'Managing', 'Founder', 'COO', 'Co-Founder,', 'Chief', 'Operations', 'Information',
                         'CSO', 'Scientific',
                         'Officer,', 'Director,', 'CTO,', 'Controller', 'Finance', 'Worldwide', "Chief", "Human",
                         "Resources", "Officer",
                         "CEO", "Customer", "Financial", "CFO", "CIO", "Engineer", "Administrator", "Developer",
                         "Board Member", "Design", "Social Media"]

team_title = ['CEO', 'Chairman', 'Director', 'Co-Founder', 'VICE PRESIDENT', 'CTO', 'Chief Executive Office', 'Head', 'Board', 'VP','V.P', 'Founder','President']
team_title_multi = ['Chief']