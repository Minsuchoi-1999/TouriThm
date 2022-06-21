1. TouriThm_setting.sh를 실행해주세요

2. 대부분은 모두 자동으로 설정되었지만, 수동으로 해주셔야하는 것들이 있습니다.

3. sudo vi /etc/profile을 입력해주세요.

4. export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64를 입력해 자바 PATH를 설정해주세요.

5. cd elasticsearch-8.2.0/를 입력해주세요.

6. vi config/elasticsearch.yml을 입력해주세요.

7. xpack.security.enabled: false, network.host: 0.0.0.0으로 설정해주세요.
