##########################################################################################
# Name: Load Terms from a CSV File
# Description:
# This demonstrates how to read a  csv file and create new terms in
# an Alation catalog.
#
# It uses term APIs and the search API. It checks for the existenace of a term before
# adding it.  It sets the term title, description, term template, and glossary.
#
# The code uses the Alation REST APIs.
#
# Author: Rishabh Gupta
# 
# Catalog Requirements:
# - The term glossary must already exist
# - The term template must alerady exist
#
#
#
##########################################################################################


import requests
import csv
import json

# initialize variables

# Please replace this with  token & base_url.
HEADERS = {'Token': 'xorFfAQaEwK-y-ERAC4ClCpxfuWxBTzg6bJ7Dmewax4'}
BASE_URL = "https://capgemini.alationcatalog.com/"
glossary_id = 25
template_id = 85
input_file = 'sample_terms.csv'
terms_processed = 0

print('Loading terms....')

try:
    # open csv file in read mode
    with open(input_file, 'r') as read_obj:
        csv_reader = csv.reader(read_obj, delimiter=",")
        header = next(csv_reader)

        if header != None:
            # Iterate over each row after the header in the csv
            for row in csv_reader:

                input_term_id = row[0]
                term_title = row[1]
                term_description = row[2]
                print(term_title,term_description)
                term_exists = False

                # check to see if the term exists
                if input_term_id != '':
                    term_url = '/integration/v2/term/'
                    parm = 'id=%s&limit=100&skip=0&deleted=false' % input_term_id
                    response = requests.get(
                        BASE_URL + term_url, params=parm, headers=HEADERS)
                    term_found = response.json()
                    if len(term_found) > 0:
                        term_exists = True
                        term_id = term_found['id']
                        print('term %s found to exist with id: %s' %
                              (term_title, str(input_term_id)))
                    else:
                        print(term_found)

                else:
                    # search for the term by name in case it already exists, if more than one is found do not update
                    term_url = '/integration/v2/term/'
                    parm = 'limit=100&skip=0&search=%s&deleted=false' % term_title
                    response = requests.get(
                        BASE_URL + term_url, params=parm, headers=HEADERS)
                    term_found = response.json()

                    if len(term_found) == 0:
                        # create term with temp name
                        term_url = '/integration/v2/term/'

                        payload = [
                            {
                                "title": term_title,
                                "description": term_description,
                                "template_id": template_id,
                                "glossary_ids": [glossary_id],
                            }
                        ]
                        response = requests.post(
                            BASE_URL + term_url, json=payload, headers=HEADERS)
                        term_result = response.json()
                        term_id = term_result['job_id']
                        print(term_result)
                        print('Term %s created' % term_title)

                    elif len(term_found) == 1:
                        term_id = term_found['results'][0]['id']
                        print('term %s found to exist with id: %s' %
                              (term_title, str(input_term_id)))

                    else:
                        print('Multiple terms named %s found to exist' %
                              term_title)

                terms_processed = terms_processed + 1
            print('Total terms processed: %s' % str(terms_processed))

except Exception as err:
    print('Can not continue.  Error: %s' % str(err))
    print('processing terminated')
    exit()

print('Loading terms finished')
