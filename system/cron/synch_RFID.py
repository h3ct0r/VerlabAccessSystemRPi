import json
import ldap
import sys
import re
from unidecode import unidecode


def main(cfg):
    l = ldap.initialize(cfg['ldap_uri'])
    try:
        l.protocol_version = ldap.VERSION3
        l.simple_bind_s(cfg['ldap_username'], cfg['ldap_passwd'])
    except Exception, error:
        sys.stderr.write(str(error))
        sys.exit()

    search_scope = ldap.SCOPE_SUBTREE  # this will scope the entire subtree under Users
    search_filter = "(&)"
    search_attribute = ['uid', 'accessToken', 'verlabActive', 'givenName']
    result_query = {}

    try:
        ldap_result_id = l.search(cfg['ldap_basedn'], search_scope, search_filter, search_attribute)
        while 1:
            result_type, result_data = l.result(ldap_result_id, 0)
            if not result_data:
                break
            else:
                if result_type == ldap.RES_SEARCH_ENTRY:
                    data_dict = result_data[0][1]

                    if not all(x in data_dict.keys() for x in search_attribute):
                        continue

                    if data_dict['verlabActive'][0] != 'TRUE':
                        continue

                    # Format data from the LDAP, use first find
                    uid = data_dict.pop('uid', None)
                    small_data = {}
                    for k in search_attribute:
                        if k in data_dict:
                            small_data[k] = unidecode(unicode(data_dict[k][0], encoding = "utf-8"))

                    result_query[uid[0]] = small_data
    except ldap.LDAPError, e:
        sys.stderr.write(str(e))
        sys.exit()

    l.unbind_s()

    #result_query.sort(key=lambda x: x['accessToken'][0])
    with open('../data/data.json', 'w') as outfile:
        json.dump(result_query, outfile)

if __name__ == "__main__":
    with open('../config/config.json') as data_file:
        config = json.load(data_file)

    main(config)
