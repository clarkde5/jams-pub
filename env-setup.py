def main():
  import os
  import sys
  from pathlib import Path

  home = str(Path.home())

  if len(sys.argv) == 2:
      rsa_private_key = sys.argv[1]
  else:
    rsa_private_key = ""
    print("PrivateKey is required")
    return

  print("PrivateKey acquired")

  Path(f"{home}/.ssh/").mkdir(parents=True, exist_ok=True)

  f = open(f"{home}/.ssh/id_rsa", "w")
  f.write(rsa_private_key)
  f.close()
  os.chmod(f"{home}/.ssh/id_rsa", 0o600)

  f = open(f"{home}/.ssh/known_hosts", "w")
  f.write("""|1|NLCeolhVq8rUb2gdHsEN1+eo0/w=|bMFE7NpV8/yfBkwt1V416Ikj43M= ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIOMqqnkVzrm0SdG6UOoqKLsabgH5C9okWi0dh2l9GKJl
  |1|Cridrc6Vr8plmuAmrnDuHNAzA4Y=|4VqfqZfFqPIIPVXRxIykjLwo5f8= ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQCj7ndNxQowgcQnjshcLrqPEiiphnt+VTTvDP6mHBL9j1aNUkY4Ue1gvwnGLVlOhGeYrnZaMgRK6+PKCUXaDbC7qtbW8gIkhL7aGCsOr/C56SJMy/BCZfxd1nWzAOxSDPgVsmerOBYfNqltV9/hWCqBywINIR+5dIg6JTJ72pcEpEjcYgXkE2YEFXV1JHnsKgbLWNlhScqb2UmyRkQyytRLtL+38TGxkxCflmO+5Z8CSSNY7GidjMIZ7Q4zMjA2n1nGrlTDkzwDCsw+wqFPGQA179cnfGWOWRVruj16z6XyvxvjJwbz0wQZ75XK5tKSb7FNyeIEs4TT4jk+S4dhPeAUC5y+bDYirYgM4GC7uEnztnZyaVWQ7B381AK4Qdrwt51ZqExKbQpTUNn+EjqoTwvqNj4kqx5QUCI0ThS/YkOxJCXmPUWZbhjpCg56i+2aB6CmK2JGhn57K5mj0MNdBXA4/WnwH6XoPWJzK5Nyu2zB3nAZp+S5hpQs+p1vN1/wsjk=
  |1|IkM+MCpqt0ao0W7cH98Gkyb2kn8=|Xbscni2Q/6zNfMw+tZl4u3y9/2s= ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBEmKSENjQEezOmxkZMy7opKgwFB9nkt5YRrYMjNuG5N87uRgg6CLrbo5wAdT/y6v0mKV0U2w0WZ2YB/++Tpockg=
  """)
  f.close()

if __name__ == "__main__":
  main()