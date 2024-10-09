#!/bin/sh
#
# Simple tool to calculate max parallel jobs based on
# memory of builder.
#
# MDCache.cc generally runs out of RAM in 4G of memory
# with parallel=4

if [ ""$(dpkg-architecture -qDEB_HOST_ARCH_BITS) = 32 ] ; then
	echo "--max-parallel=1"
	exit 0
fi

total_ram=$(grep MemTotal /proc/meminfo | awk '{ print $2 }')

fivehundred_g=$((512*1024*1024))
twohundredtwentysix_g=$((256*1024*1024))
hundredtwenty_g=$((128*1024*1024))
nightysix_g=$((96*1024*1024))
sixtyfour_g=$((64*1024*1024))
fourtyheight_g=$((48*1024*1024))
thirtytwo_g=$((32*1024*1024))
sixteen_g=$((16*1024*1024))
eight_g=$((8*1024*1024))
four_g=$((4*1024*1024))

if [ ${total_ram} -le ${four_g} ]; then
    echo "--max-parallel=1"
elif [ ${total_ram} -le ${eight_g} ]; then
    echo "--max-parallel=2"
elif [ ${total_ram} -le ${sixteen_g} ]; then
    echo "--max-parallel=3"
elif [ ${total_ram} -le ${thirtytwo_g} ]; then
    echo "--max-parallel=12"
elif [ ${total_ram} -le ${fourtyheight_g} ]; then
    echo "--max-parallel=20"
elif [ ${total_ram} -le ${sixtyfour_g} ]; then
    echo "--max-parallel=32"
elif [ ${total_ram} -le ${nightysix_g} ]; then
    echo "--max-parallel=48"
elif [ ${total_ram} -le ${hundredtwenty_g} ]; then
    echo "--max-parallel=64"
elif [ ${total_ram} -le ${twohundredtwentysix_g} ]; then
    echo "--max-parallel=128"
elif [ ${total_ram} -le ${fivehundred_g} ]; then
    echo "--max-parallel=256"
else
    echo "--max-parallel=512"
fi
