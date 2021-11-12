export MVN_HOME=__MVN_HOME__
export PATH=$PATH:$MVN_HOME/bin

export HADOOP_HOME=__HADOOP_HOME__
export HADOOP_COMMON_LIB_NATIVE_DIR=$HADOOP_HOME/lib/native
export HADOOP_OPTS="$HADOOP_OPTS -Djava.library.path=$HADOOP_HOME/lib/native"
export HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop
export PATH=$PATH:${HADOOP_HOME}/bin:${HADOOP_HOME}/sbin

export HBASE_HOME=__HBASE_HOME__
export HBASE_CONF_DIR=$HBASE_HOME/conf
#export HBASE_HOME=/home/brad/hbase-2.2.6
export PATH=$PATH:${HBASE_HOME}/bin

export ZK_HOME=__ZK_HOME__
export PATH=$PATH:$ZK_HOME/bin

export PHOENIX_HOME=__PHOENIX_HOME__
export PHOENIX_CLASSPATH=$PHOENIX_HOME
export PATH=$PHOENIX_HOME/bin:$PATH
