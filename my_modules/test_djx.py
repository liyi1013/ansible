#!coding = utf-8
# 测试配置文件的读写

class RedHatStrategy():

    NETWORK_FILE = './network'

    def get_permanent_hostname(self):
        try:
            f = open(self.NETWORK_FILE, 'rb')
            try:
                for line in f.readlines():
                    if line.startswith('HOSTNAME'):
                        k, v = line.split('=')
                        print(v)
                        print(v.strip())
                        return v.strip()
            finally:
                f.close()
        except Exception:
            pass 
            #err = get_exception()
            #self.module.fail_json(msg="failed to read hostname: %s" str(err))
    def set_permanent_hostname(self, name):
        try:
            lines = []
            found = False
            f = open(self.NETWORK_FILE, 'rb')
            try:
                for line in f.readlines():
                    if line.startswith('HOSTNAME'):
                        lines.append("HOSTNAME=%s\n" % name)
                        found = True
                    else:
                        lines.append(line)
            finally:
                f.close()
            if not found:
                lines.append("HOSTNAME=%s\n" % name)
            f = open(self.NETWORK_FILE, 'w+')
            try:
                f.writelines(lines)
            finally:
                f.close()
        except Exception:
            err = 'error' #get_exception()
            #self.module.fail_json(msg="failed to update hostname: %s" %
             #   str(err))

def main():
    a=RedHatStrategy()
    a.get_permanent_hostname()

if __name__ == '__main__':
    main()