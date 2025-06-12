# financialwork

## Windows setup

If running `docker-compose up` on Windows fails with
`/usr/bin/env: 'bash\r': No such file or directory`, ensure that
shell scripts use LF line endings. The repository includes a
`.gitattributes` file that forces `*.sh` files to use LF so you may need to re-checkout the project or run `git rm --cached -r . && git reset --hard` if line endings were previously converted.
