#!/usr/bin/env sh

mkdir -p img

for i in `seq 0 9` n; do
	mogrify -background transparent -format png svg/$i.svg
	mv svg/$i.png img/
done
