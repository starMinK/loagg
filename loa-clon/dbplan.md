DB 계획
=============
1. 장비 - 덕현, 종열, 상륜
    * profileInfo: 상륜
    * characterImage: 종열
    * characterInfo: 덕현
      * profile-ability-basic: 기본 특성
        * 공격력 100
          * int atk : 공격력 / 2 + 300
          * 
      * profile-ability-battle: 전투 특성
      * profile-ability-engrave: 각인 효과
        * 1번
        * 2번
        * 3번
        * 4번
        * 5번
      * profile-ability-tendency: 성향
        * 지성
        * 담력
        * 매력
        * 친절

---

2. 보석 - 규민
   * jewel-slot0
     * name
     * img
     * tear
     * trade
     * lv
     * skill-effect
     
     *if lv > class*

  * jewel-slot1
    * jewel-slot0
    * name
    * img
    * tear
    * trade
    * lv
    * skill-effect
     
    *if lv > class*

  * jewel-slot2
    * jewel-slot0
    * name
    * img
    * tear
    * trade
    * lv
    * skill-effect
     
    *if lv > class*

  * jewel-slot3
    * jewel-slot0
    * name
    * img
    * tear
    * trade
    * lv
    * skill-effect
     
    *if lv > class*

  * jewel-slot4
    * 위랑 동일
  * jewel-slot5
    * 위랑 동일
  * jewel-slot6
    * 위랑 동일
  * jewel-slot7
    * 위랑 동일
  * jewel-slot8
    * 위랑 동일
  * jewel-slot9
    * 위랑 동일
  * jewel-slot10
    * 위랑 동일

---

3. 카드 - 재하

---

1. search.html -> 이름 받기 -> db저장
    * function save_name -> index.html line 140 cf
    * py -> db.insert (name) -> 등록
2. jewel.py -> 이름을 db에서 get -> 받아온 이름으로 크롤링
    * list(db.jewel.find) -> name get
    * 크롤링/{name} -> 크롤링 정보 get
    * db에 저장?
3. 크롤링된 정보들 -> db에 이름이 ?인 곳에 수정으로 내용 추가
4. main.html -> db에서 이름으로 정보 불러오기


