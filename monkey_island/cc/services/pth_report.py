from cc.services.pth_report_utils import PassTheHashReport, Machine


class PTHReportService(object):

    """

    """

    def __init__(self):
        pass

    @staticmethod
    def get_duplicated_password_nodes(pth):
        """

        """

        usernames_lists = []
        usernames_per_sid_list = []
        dups = dict(map(lambda x: (x, len(pth.GetSidsBySecret(x))), pth.GetAllSecrets()))

        for secret, count in sorted(dups.iteritems(), key=lambda (k, v): (v, k), reverse=True):
            if count <= 1:
                continue
            for sid in pth.GetSidsBySecret(secret):
                usernames_per_sid_list.append(pth.GetUsernameBySid(sid))

            usernames_lists.append({'cred_group': usernames_per_sid_list})

        return usernames_lists

    @staticmethod
    def get_shared_local_admins_nodes(pth):
        dups = dict(map(lambda x: (x, len(pth.GetSharedAdmins(x))), pth.machines))
        shared_admin_machines = []
        for m, count in sorted(dups.iteritems(), key=lambda (k, v): (v, k), reverse=True):
            if count <= 0:
                continue
            shared_admin_account_list = []

            for sid in pth.GetSharedAdmins(m):
                shared_admin_account_list.append(pth.GetUsernameBySid(sid))

            machine = {
                'ip': m.GetIp(),
                'hostname': m.GetHostName(),
                'domain': m.GetDomainName(),
                'services_names': m.GetCriticalServicesInstalled(),
                'user_count': count,
                'admins_accounts': shared_admin_account_list
            }

            shared_admin_machines.append(machine)

        return shared_admin_machines

    @staticmethod
    def get_strong_users_on_crit_services(pth):
        threatening = dict(map(lambda x: (x, len(pth.GetThreateningUsersByVictim(x))), pth.GetCritialServers()))
        strong_users_crit_list = []

        for m, count in sorted(threatening.iteritems(), key=lambda (k, v): (v, k), reverse=True):
            if count <= 0:
                continue

            threatening_users_attackers_dict = {}
            for sid in pth.GetThreateningUsersByVictim(m):
                username = pth.GetUsernameBySid(sid)
                threatening_users_attackers_dict[username] = []
                for mm in pth.GetAttackersBySid(sid):
                    if m == mm:
                        continue
                    threatening_users_attackers_dict[username] = mm.GetIp()

            machine = {
                'ip': m.GetIp(),
                'hostname': m.GetHostName(),
                'domain': m.GetDomainName(),
                'services_names': m.GetCriticalServicesInstalled(),
                'user_count': count,
                'threatening_users': threatening_users_attackers_dict
            }
            strong_users_crit_list.append(machine)
        return strong_users_crit_list

    @staticmethod
    def get_strong_users_on_non_crit_services(pth):
        threatening = dict(map(lambda x: (x, len(pth.GetThreateningUsersByVictim(x))), pth.GetNonCritialServers()))

        strong_users_non_crit_list = []

        for m, count in sorted(threatening.iteritems(), key=lambda (k, v): (v, k), reverse=True):
            if count <= 0:
                continue

            threatening_users_attackers_dict = {}
            for sid in pth.GetThreateningUsersByVictim(m):
                username = pth.GetUsernameBySid(sid)
                threatening_users_attackers_dict[username] = []
                for mm in pth.GetAttackersBySid(sid):
                    if m == mm:
                        continue
                    threatening_users_attackers_dict[username] = mm.GetIp()

            machine = {
                'ip': m.GetIp(),
                'hostname': m.GetHostName(),
                'domain': m.GetDomainName(),
                'services_names': [],
                'user_count': count,
                'threatening_users': threatening_users_attackers_dict
            }
            strong_users_non_crit_list.append(machine)
        return strong_users_non_crit_list

    @staticmethod
    def get_duplicated_passwords_issues(pth, password_groups):
        issues = []
        for group in password_groups:
            username = group['cred_group'][0]
            sid = list(pth.GetSidsByUsername(username.split('\\')[1]))
            machine_info = pth.GetSidInfo(sid[0])
            issues.append(
                {
                    'type': 'shared_passwords',
                    'machine': machine_info.get('hostname').split('.')[0],
                    'shared_with': group['cred_group']
                }
            )

        return issues

    @staticmethod
    def get_shared_local_admins_issues(shared_admins_machines):
        issues = []
        for machine in shared_admins_machines:
            issues.append(
                {
                    'type': 'shared_admins',
                    'machine': machine.get('hostname'),
                    'shared_accounts': machine.get('admins_accounts'),
                    'ip': machine.get('ip'),
                }
            )

        return issues

    @staticmethod
    def strong_users_on_crit_issues(strong_users):
        issues = []
        for machine in strong_users:
            issues.append(
                {
                    'type': 'strong_users_on_crit',
                    'machine': machine.get('hostname'),
                    'services': machine.get('services_names'),
                    'ip': machine.get('ip'),
                    'threatening_users': machine.get('threatening_users')
                }
            )

        return issues

    @staticmethod
    def generate_map_nodes(pth):
        nodes_list = []
        for node_id in pth.vertices:
            machine = Machine(node_id)
            node = {
                "id": str(node_id),
                "label": '{0} : {1}'.format(machine.GetHostName(), machine.GetIp()),
                'group': 'critical' if machine.IsCriticalServer() else 'normal',
                'users': list(machine.GetCachedUsernames()),
                'ips': [machine.GetIp()],
                'services': machine.GetCriticalServicesInstalled(),
                'hostname': machine.GetHostName()
            }
            nodes_list.append(node)

        return nodes_list

    @staticmethod
    def get_issues_list(issues):
        issues_dict = {}

        for issue in issues:
            machine = issue['machine']
            if machine not in issues_dict:
                issues_dict[machine] = []
            issues_dict[machine].append(issue)

        return issues_dict

    @staticmethod
    def get_report():

        issues = []
        pth = PassTheHashReport()

        same_password = PTHReportService.get_duplicated_password_nodes(pth)
        local_admin_shared = PTHReportService.get_shared_local_admins_nodes(pth)
        strong_users_on_crit_services = PTHReportService.get_strong_users_on_crit_services(pth)
        strong_users_on_non_crit_services = PTHReportService.get_strong_users_on_non_crit_services(pth)

        issues += PTHReportService.get_duplicated_passwords_issues(pth, same_password)
        issues += PTHReportService.get_shared_local_admins_issues(local_admin_shared)
        issues += PTHReportService.strong_users_on_crit_issues(strong_users_on_crit_services)
        #formated_issues = PTHReportService.get_issues_list(issues)

        report = \
            {
                'report_info':
                    {
                        'same_password': same_password,
                        'local_admin_shared': local_admin_shared,
                        'strong_users_on_crit_services': strong_users_on_crit_services,
                        'strong_users_on_non_crit_services': strong_users_on_non_crit_services,
                        'pth_issues': issues
                    },
                'pthmap':
                    {
                        'nodes': PTHReportService.generate_map_nodes(pth),
                        'edges': pth.edges
                    }
            }
        return report

        # print """<div class="hidden">"""
        #
        # print "<h2>Cached Passwords</h2>"
        # print "<h3>On how many machines each secret is cached (possible attacker count)?</h3>"
        # cache_counts = dict(map(lambda x: (x, pth.GetAttackCountBySecret(x)), pth.GetAllSecrets()))
        #
        # print """<table>"""
        # print """<tr><th>Secret</th><th>Machine Count</th></tr>"""
        # for secret, count in sorted(cache_counts.iteritems(), key=lambda (k,v): (v,k), reverse=True):
        #     if count <= 0:
        #         continue
        #     print """<tr><td><a href="#{secret}">{secret}</a></td><td>{count}</td>""".format(secret=secret, count=count)
        # print """</table>"""
        #
        # print "<h2>User's Creds</h2>"
        # print "<h3>To how many machines each user is able to connect with admin rights</h3>"
        # attackable_counts = dict(map(lambda x: (x, pth.GetVictimCountBySid(x)), pth.GetAllSids()))
        #
        # print """<table>"""
        # print """<tr><th>SID</th><th>Username</th><th>Machine Count</th></tr>"""
        # for sid, count in sorted(attackable_counts.iteritems(), key=lambda (k,v): (v,k), reverse=True):
        #     if count <= 1:
        #         continue
        #     print """<tr><td><a href="#{sid}">{sid}</a></td><td>{username}</td><td>{count}</td>""".format(sid=sid, username=pth.GetUsernameBySid(sid), count=count)
        # print """</table>"""
        #
        # print "<h2>Actual Possible Attacks By SID</h2>"
        # print "<h3>How many attacks possible using each SID (aka len(attacker->victim pairs))</h3>"
        # possible_attacks_by_sid = dict(map(lambda x: (x, pth.GetPossibleAttackCountBySid(x)), pth.GetAllSids()))
        #
        # print """<table>"""
        # print """<tr><th>SID</th><th>Username</th><th>Machine Count</th></tr>"""
        # for sid, count in sorted(possible_attacks_by_sid.iteritems(), key=lambda (k,v): (v,k), reverse=True):
        #     if count <= 1:
        #         continue
        #     print """<tr><td><a href="#{sid}">{sid}</a></td><td>{username}</td><td>{count}</td>""".format(sid=sid, username=pth.GetUsernameBySid(sid), count=count)
        # print """</table>"""
        #
        # print "<h2>Machine's Creds</h2>"
        # print "<h3>To how many machines each machine is able to directly connect with admin rights?</h3>"
        # attackable_counts = dict(map(lambda m: (m, pth.GetVictimCountByMachine(m)), pth.machines))
        #
        # print """<table>"""
        # print """<tr><th>Attacker Ip</th><th>Attacker Hostname</th><th>Domain Name</th><th>Victim Machine Count</th></tr>"""
        # for m, count in sorted(attackable_counts.iteritems(), key=lambda (k,v): (v,k), reverse=True):
        #     if count <= 1:
        #         continue
        #     print """<tr><td><a href="#{ip}">{ip}</a></td><td>{hostname}</td><td>{domain}</td><td>{count}</td>""".format(ip=m.GetIp(), hostname=m.GetHostName(), domain=m.GetDomainName(), count=count)
        # print """</table>"""
        #
        # print "<h2>Domain Controllers</h2>"
        # print "<h3>List of domain controllers (we count them as critical points, so they are listed here)</h3>"
        # DCs = dict(map(lambda m: (m, pth.GetInPathCountByVictim(m)), pth.GetAllDomainControllers()))
        #
        # print """<table>"""
        # print """<tr><th>DC Ip</th><th>DC Hostname</th><th>Domain Name</th><th>In-Path Count</th></tr>"""
        # for m, path_count in sorted(DCs.iteritems(), key=lambda (k,v): (v,k), reverse=True):
        #     print """<tr><td><a href="#{ip}">{ip}</a></td><td><a href="#{ip}">{hostname}</a></td><td>{domain}</td><td>{path_count}</td></tr>""".format(ip=m.GetIp(), hostname=m.GetHostName(), domain=m.GetDomainName(), path_count=path_count)
        # print """</table>"""
        #
        # print "<h2>Most Vulnerable Machines</h2>"
        # print "<h3>List all machines in the network sorted by the potincial to attack them</h3>"
        # all_machines = dict(map(lambda m: (m, pth.GetInPathCountByVictim(m)), pth.machines))
        #
        # print """<table>"""
        # print """<tr><th>Ip</th><th>Hostname</th><th>Domain Name</th><th>In-Path Count</th></tr>"""
        # for m, path_count in sorted(all_machines.iteritems(), key=lambda (k,v): (v,k), reverse=True):
        #     if count <= 0:
        #         continue
        #     print """<tr><td><a href="#{ip}">{ip}</a></td><td><a href="#{ip}">{hostname}</a></td><td>{domain}</td><td>{path_count}</td></tr>""".format(ip=m.GetIp(), hostname=m.GetHostName(), domain=m.GetDomainName(), path_count=path_count)
        # print """</table>"""
        #
        # print "<h2>Critical Servers</h2>"
        # print "<h3>List of all machines identified as critical servers</h3>"
        # critical_servers = pth.GetCritialServers()
        #
        # print """<table>"""
        # print """<tr><th>Ip</th><th>Hostname</th><th>Domain Name</th></tr>"""
        # for m in critical_servers:
        #     print """<tr><td><a href="#{ip}">{ip}</a></td><td><a href="#{ip}">{hostname}</a></td><td>{domain}</td></tr>""".format(ip=m.GetIp(), hostname=m.GetHostName(), domain=m.GetDomainName())
        # print """</table>"""
        #
        # print "<hr />"
        #
        # for m in pth.machines:
        #     print """<a name="{ip}"><h2>Machine '{ip}'</h2></a>
        #              <h3>Hostname '{hostname}'</h3>""".format(ip=m.GetIp(), hostname=m.GetHostName())
        #
        #     print """<h3>Cached SIDs</h3>"""
        #     print """<h4>SIDs cached on this machine</h4>"""
        #     print """<ul>"""
        #     for sid in pth.GetCachedSids(m):
        #         print """<li><a href="#{sid}">{username} ({sid})</a></li>""".format(username=pth.GetUsernameBySid(sid), sid=sid)
        #     print """</ul>"""
        #
        #     print """<h3>Possible Attackers</h3>"""
        #     print """<h4>Machines that can attack this machine</h4>"""
        #     print """<ul>"""
        #     for attacker in pth.GetAttackersByVictim(m):
        #         print """<li><a href="#{ip}">{ip} ({hostname})</a></li>""".format(ip=attacker.GetIp(), hostname=attacker.GetHostName())
        #     print """</ul>"""
        #
        #
        #     print """<h3>Admins</h3>"""
        #     print """<h4>Users that have admin rights on this machine</h4>"""
        #     print """<ul>"""
        #     for sid in m.GetAdmins():
        #         print """<li><a href="#{sid}">{username} ({sid})</a></li>""".format(username=m.GetUsernameBySid(sid), sid=sid)
        #     print """</ul>"""
        #
        #     print """<h3>Installed Critical Services</h3>"""
        #     print """<h4>List of crtical services found installed on machine</h4>"""
        #     print """<ul>"""
        #     for service_name in m.GetCriticalServicesInstalled():
        #         print """<li>{service_name}</li>""".format(service_name=service_name)
        #     print """</ul>"""
        #
        #
        # print "<hr />"
        #
        # for username in pth.GetAllUsernames():
        #     print """<a name="{username}"><h2>User '{username}'</h2></a>""".format(username=username)
        #
        #     print """<h3>Matching SIDs</h3>"""
        #     print """<ul>"""
        #     for sid in pth.GetSidsByUsername(username):
        #         print """<li><a href="#{sid}">{username} ({sid})</a></li>""".format(username=pth.GetUsernameBySid(sid),
        #                                                                             sid=sid)
        #     print """</ul>"""
        #
        # print "<hr />"
        #
        # for sid in pth.GetAllSids():
        #     print """<a name="{sid}"><h2>SID '{sid}'</h2></a>
        #             <h3>Username: '<a href="#{username}">{username}</a>'</h3>
        #             <h3>Domain: {domain}</h3>
        #             <h3>Secret: '<a href="#{secret}">{secret}</a>'</h3>
        #           """.format(username=pth.GetUsernameBySid(sid), sid=sid, secret=pth.GetSecretBySid(sid),
        #                      domain=pth.GetSidInfo(sid)["Domain"])
        #
        #     print """<h3>Machines the sid is local admin on</h3>"""
        #     print """<ul>"""
        #     for m in pth.GetVictimsBySid(sid):
        #         print """<li><a href="#{ip}">{ip} ({hostname})</a></li>""".format(ip=m.GetIp(), hostname=m.GetHostName())
        #     print """</ul>"""
        #
        #     print """<h3>Machines the sid is in thier cache</h3>"""
        #     print """<ul>"""
        #     for m in pth.GetAttackersBySid(sid):
        #         print """<li><a href="#{ip}">{ip} ({hostname})</a></li>""".format(ip=m.GetIp(), hostname=m.GetHostName())
        #     print """</ul>"""
        #
        # for secret in pth.GetAllSecrets():
        #     print """<a name="{secret}"><h2>Secret '{secret}'</h2></a>""".format(secret=secret)
        #
        #     print """<h3>SIDs that use that secret</h3>"""
        #     print """<ul>"""
        #     for sid in pth.GetSidsBySecret(secret):
        #         print """<li><a href="#{sid}">{username} ({sid})</a></li>""".format(username=pth.GetUsernameBySid(sid),
        #                                                                             sid=sid)
        #     print """</ul>"""
        #
        #     print """<h3>Attackable Machines with that secret</h3>"""
        #     print """<ul>"""
        #     for m in pth.GetVictimsBySecret(secret):
        #         print """<li><a href="#{ip}">{hostname}</a></li>""".format(ip=m.GetIp(), hostname=m.GetHostName())
        #     print """</ul>"""
        #
        #     print """<h3>Machines that have this secret cached and can use it to attack other machines</h3>"""
        #     print """<ul>"""
        #     for m in pth.GetAttackersBySecret(secret):
        #         print """<li><a href="#{ip}">{hostname}</a></li>""".format(ip=m.GetIp(), hostname=m.GetHostName())
        #     print """</ul>"""
