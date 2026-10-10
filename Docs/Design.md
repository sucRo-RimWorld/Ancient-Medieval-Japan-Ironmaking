# AMJ Ironmaking — 古代・中世製鉄設計

**Authority:** This file is the Ironmaking owner design. The Project's former design is migration history/pointer only.
**Provenance:** Project `Docs/Research/IronmakingDesign.md` (2026-10-10); earlier Grains design.

設計正本移管: 2026-10-10 JST  
状態: 作者確定コンセプト + 詳細設計案。最小開発用XML実装済み。Vanillaの限定5項目Pickle実機E2EはPASSしたが、製錬Bill実行・実機バランス・MO互換・正式配布は未検証。

## 1. 確定コンセプト

独立Modとして古代から中世の製鉄を扱う。仮称は **Ancient & Medieval Japan - Ironmaking**。江戸・近世の完成型は実装しない。既存の鍛冶・鉄器加工を置き換えるModではなく、**既存の鍛冶へ、日本式の鉄自給ルートを追加するMod**とする。鍛冶技術の成立を前段階に置き、初期製鉄から炉の改良を経て、中世段階のたたらを上位研究に置く。

Grains、Environment、Waterworks、Medieval Overhaul (MO) を必須依存にしない。主要ループはVanilla + Ironmakingだけで成立させ、他Modは公式任意互換とする。刀剣・甲冑の大量追加、超能力名刀、汎用修理・再利用は所有しない。

この文書は確定事項と提案を区別する。具体的なpackageId / DefName、設備寸法、性能、数量、研究費は未確定。ここでの仮称・数値を公開契約や実装済み仕様として扱わない。

## 2. 旧鉄資源案との整合

旧Designの「Japanese Iron ResourcesはMO必須で一次製錬まで所有」「Japanese Ironworkingは低優先度保留」は、今回の独立Ironmaking方針に置き換える。

| 領域 | 現在の所有方針 |
|---|---|
| 砂鉄という資源、単体で成立する最低限の採取・供給 | Ironmaking |
| 炭化、初期炉、中世炉、送風、製錬・鉄材化 | Ironmaking |
| マップ・地域に応じた最低限の砂鉄アクセス差 | Ironmaking。Vanilla地形でも成立させる |
| MO既存の鉄鉱床・Mine Shaft等の鉄鉱石供給 | Ironmaking単体では変更しない。MO + Japanization + Ironmakingの統合構成ではJapanizationが供給量・露出を再調整し、砂鉄を主要ルート、鉄鉱石を副次ルートとして成立させる |
| 気候・植生・土壌等の環境データ | Environment。鉄資源や製鉄そのものは必須責務にしない |
| 一般水路、取水、配水、他機能への水利接続 | Waterworks |
| 砂鉄洗浄等の製鉄専用加工 | Ironmaking。水利データ利用は任意互換 |
| 装備完成品、武器固有能力 | 別機能または既存Mod互換 |
| 装備修理・資源回収 | 既存汎用Mod優先。製鉄開始の前提にしない |

旧Iron Resourcesを同時公開する義務、MO必須条件、MO炉へ砂鉄Billを追加することだけで一次製錬を済ませる条件は撤回する。別の資源分布Modを作るかは未決定であり、新たなハード依存を作らない。既存のVanilla/MO鉱床や通常製鉄は、Ironmakingの導入だけで減らしたり消したりしない。

**MO + Ironmakingだけの構成では、MOの鉄鉱床とAMJ砂鉄採取地点を併存させる。** Ironmakingは他Mod所有の資源生成を勝手に弱体化しない。一方、`AMJ - Medieval Overhaul Japanization` まで導入した日本再構成プロファイルでは、JapanizationがMO所有の鉄資源供給を調整する。ここでは砂鉄を日本式製鉄の主要自然資源とし、MO鉄鉱石は削除せず副次的な供給源として残す。地表鉱床だけでなく、反復可能なMine Shaftの鉄鉱石Recipeも総供給量の一部として同時に監査・調整する。正確な出現率、鉱脈サイズ、Mine Shaftの作業量/出力/研究位置は未確定で、実測バランス後に決める。

## 3. 研究進行

ゲーム上の進行は **既存の鍛冶・鉄器加工 → 初期製鉄 → 製鉄炉の改良 → 中世たたら製鉄** とする。**「鉄器加工」はIronmaking独自の研究ノードとして重複追加しない。** Vanillaでは既存 `Smithing` を前段階の基準とし、MO併用時も既存の鍛冶研究を利用する。Japanization併用時だけ、MO側研究の名称・位置・前提関係を日本史に合わせて再構成する。

| 段階 | 所有 | 役割 |
|---|---|---|
| 既存の鍛冶・鉄器加工 | Vanilla / MO | 既存鉄材を加工できる段階。国内製鉄の自給は保証しない |
| 初期製鉄 | Ironmaking | 小型炉と砂鉄製錬を解禁し、一般鉄材を自給可能にする |
| 製鉄炉の改良 | Ironmaking | 中規模操業、歩留まり・燃料効率・作業効率を改善する |
| 中世たたら製鉄 | Ironmaking | 大規模操業、発達した炉床・防湿・送風を抽象化し、後期の高品質材選別へ接続する |

研究費・技能要件は実装前のバランステストで決める。研究ノードを増やして技術史の全工程を一覧化しない。

「箱形炉製鉄」を独立研究名にはしない。箱形炉は古代から確認され、竪形炉との地域差もあるため、全国一律に「初期炉の次に箱形炉へ進歩した」と表現しない。中段研究は **製鉄炉の改良** とし、箱形炉を代表的な設備表現の一つとして利用できる。

初期鍛冶と製錬は分ける。鉄を利用できても鉄を自給できるとは限らない。ただしVanillaの既存鍛冶・武器・Steel利用を全面的に研究ロックしない。独自研究はAMJの追加設備・工程だけを解禁する。**MO単独併用時はMO既存研究をIronmaking側から改変せず、`AMJ - Medieval Overhaul Japanization` 併用時だけJapanizationがMO研究フローを日本史に合わせて再構成し、Ironmaking研究との接続を担当する。**

史実上の地域・年代を一本の必然的な発展順序と断定しない。この研究順は、炉規模・操業効率・供給能力の向上をRimWorld向けに抽象化したもの。

## 4. 資源・加工フロー初稿

### 共通の工程

v1の標準ループは意図的に短くする。

- 木材 → 炭化 → 木炭相当燃料。
- 砂鉄採取 → 砂鉄。
- 砂鉄 + 燃料 → 鉄塊。
- 鉄塊 → 鍛錬 → 一般鉄材。

**v1で必須の新規在庫は、砂鉄・鉄塊・Base用木炭相当燃料の3種までを原則とする。** 銑、鉄滓、良質鋼/和鋼等は、別工程や下流用途が実際にゲーム上の選択を生む段階まで追加しない。歴史用語を再現するだけの中間在庫を増やさない。

「鉧」は広い意味で鉄塊を指し得るため、たたら研究で初めて鉧という物質が出現する設計にはしない。後期の良質鋼を追加する場合も、銑 → 鉧 → 玉鋼の固定直列チェーンにはしない。

良質鋼/和鋼を将来追加する場合、**汎用Metallic Stuffとして全建築・全武器に使用可能にはしない**。明確な下流消費先を持つ特殊素材または明示Recipe用材料として追加し、単純な万能上位Steel化を避ける。

### Base / MO 所有案

| 対象 | Vanilla + Ironmaking | MO + Ironmaking |
|---|---|---|
| 砂鉄 / 鉄塊 / 必要になった場合の銑 | AMJ所有 | 同じAMJ資源 |
| 木炭相当燃料 | AMJ木炭を所有 | AMJ木炭Defは保持するが通常生産は抑制し、MO `DankPyon_Coal` を標準燃料として受け入れる方針 |
| 一般鉄材の出口 | Vanilla `Steel` をゲーム上の汎用金属の代理として利用する初稿 | `DankPyon_IronIngot` へ合流する初稿 |
| 良質鋼 | AMJ特殊素材 | 同じAMJ特殊素材。MO `Steel` を上書きしない |
| AMJ炉・研究 | Ironmakingが所有 | 同じAMJ炉・研究。MO製鉄は並存 |
| MOのIron Ingot → Steel | 存在しない | MOが所有。MO単独では現行工程を保持し、Japanization併用時の研究位置・前提接続はJapanizationが調整 |

BaseでSteelを出口にするのは「古代の鍛錬鉄が現代の均質鋼と同じ」という歴史主張ではなく、Vanillaの建設・加工へ接続するゲーム上の代理。AMJ独自錬鉄をStuffとして残す案も比較対象だが、単体で使える出口を失わせない。

MOではAMJの一般鉄材から直接Steelを得る標準短絡Recipeを置かない。MO単独併用ではIronIngot以降のMO工程を保持する。**Japanization併用時は、MOの `Alchemy -> Steel` 等の研究接続を日本史に合わせて組み替えるが、砂鉄採取・炉・製錬・鍛錬というIronmaking固有ゲームループはIronmakingが所有する。** Japanization側でMO経路を非表示化・再配置する場合も、Ironmaking未導入構成を含めて代替進行が成立するか別途検証する。

### MO鉄鉱床と砂鉄採取地点の両立

構成ごとに責務を分ける。

- **Vanilla + Ironmaking:** AMJ砂鉄採取地点がIronmaking側の主要自然鉄資源になる。
- **MO + Ironmaking:** MO鉄鉱床 / Mine ShaftとAMJ砂鉄をそのまま併存させる。IronmakingはMO資源生成を変更しない。
- **MO + Japanization + Ironmaking:** JapanizationがMO側の供給量・通常露出を再調整し、**砂鉄を主要ルート、鉄鉱石を副次ルート**として成立させる。鉄鉱石そのものは削除しない。
- 両ルートは一般鉄材で合流できるが、採取環境と前工程を別に保つ。砂鉄ルートが単なる余分な鉄供給源にならないよう、地表鉱床・Mine Shaft・交易等を含む総供給量でバランスを取る。
- Japanization単独でIronmakingがない構成では、代替鉄供給を失わないようMO鉄鉱石経路を実用可能な状態に保つ。

玉鋼に相当する良質鋼は一般Steelの全用途・全能力を上回る万能素材にしない。少量・高工数の特殊鍛造素材として扱う。完成品Modがなくても、一般鉄材生産が主要ループとして成立することを必須とする。良質鋼の標準用途は、取引に加えて既存刃物等への限定Recipe接続を検討するが、対応完成品・性能・品質制御は未確定。

史料は「玉鋼」という名称自体を明治期の呼称としている。機能コンセプトは維持するが、ゲーム内正式ラベルは「良質鋼」「和鋼」等も比較し、日本語説明の作者承認で確定する。「玉鋼」を採る場合も中世当時の名称と説明しない。近世鉧押しの完成形・等級体系を中世へそのまま移植しない。

## 5. 設備と数値の初期候補

| 設備 | 主な役割 | 上位設備との差別化 |
|---|---|---|
| 炭焼き設備 | 木材を製鉄燃料へ変える | v1はBill式を第一候補とし、PF等の外部Frameworkを必須にしない |
| 鍛錬設備 | 鉄塊を一般鉄材へ仕上げる | Vanilla/MOの既存鍛冶設備を再利用できる場合は重複設備を増やさない |
| 小型製鉄炉 | 少量・低投資の鉄自給 | 小さいバッチ、低い建設費、短い準備、低い歩留まり。後半でも少量処理・遠隔地・原料不足時に残る |
| 改良製鉄炉 | 日常的な中規模操業 | 中程度のバッチと設備投資。小型炉より燃料・作業効率を改善し、通常生産の中心になる |
| 中世たたら | 大量原料をまとめて処理する大規模操業 | 大バッチ、高い建設/準備負担、長い操業。単位原料当たりの効率と総スループットが高く、将来の良質材選別へ接続する |

炉の上位化は単なる完全上位互換にしない。小型炉は低投資・少量生産、改良炉は汎用、中世たたらは大口操業という**最適操業規模の違い**を持たせる。

基礎送風は各炉の操業に内包し、別ポーンを常時割り当てることを隠れた必須条件にしない。鞴などの補助設備を追加する場合は、任意の作業速度/効率補助として扱う。VFE Medieval 2等が持つForge Bellowsのような外部Linkableは互換候補にはできるが、Ironmakingの必須依存にはしない。

Baseに粘土がない場合、最低限の炉だけのために粘土採掘体系を増やさない。Vanilla木・石等による施工抽象化を第一候補とし、Clayを正式利用する際は所有Mod・取得経路・最小依存を別途監査する。MO Clayの実DefNameは本調査では未確定。

以下は静的比較用の仮数量で、史実重量比でも採用済みRecipeでもない。砂鉄・燃料・鉄塊の各1個は別々のゲーム単位。**v1の製鉄炉では燃料をBill材料として消費し、同じ操業でRefuelable燃料を二重消費しない方針を基本とする。** 炉壁破壊・再築や炉床補修は史実上重要でも、毎バッチ建物を再建させるマイクロ管理にはせず、まずWorkAmount・設備投資へ抽象化する。

| 比較用Recipe候補 | 砂鉄 | 木炭相当燃料 | 鉄塊出力 | 目的 |
|---|---:|---:|---:|---|
| 小型炉 | 40 | 60 | 10 | 小さな初期投資と少量自給 |
| 箱形炉 | 40 | 50 | 14 | 歩留まりと燃料効率の改善 |
| 中世炉・一般材優先操業 | 80 | 80 | 32 | 大口原料の効率利用 |

共通鍛錬候補は鉄塊10 → 一般鉄材8。出力/砂鉄は0.20 → 0.28 → 0.32、燃料/一般鉄材は7.50 → 約4.46 → 3.125となる（端数繰越または整数バッチ調整前の分析値）。規模が上がるほど効率は上げるが、必要原料のまとまった量、建設投資、作業量・運搬負担が増える。

作業量、木材→燃料比、良質鋼・銑の同時出力率、炉再築費は未設定。従ってこれだけで総生産効率やMO比の優劣を確定しない。MO燃料はfuelValueも異なるので、Base木炭の1個とMO Coalの1個を無条件に等価扱いしない。

中世炉の良質鋼優先Recipeは一般鉄材優先Recipeと別選択にする候補。良質鋼を増やすほど一般鉄材・燃料・技能・作業時間のいずれかで代償を持たせる。同じ鉄塊から全量の一般材と良質鋼を二重回収しない。高技能で常に最高品質の完成品を保証する仕様は置かない。

## 6. 砂鉄供給

### 6.1 基本形

砂鉄は **有限の自然資源** と **交易による補完** を基本とする。全ての土・砂・砂利から無制限に砂鉄を生成する仕様は採用しない。

新規マップでは、IronmakingがVanillaだけでも取得できる地形・ワールド情報から「砂鉄適性」を算出し、適性に応じて有限の **砂鉄堆積** を配置する。河川・海岸・砂礫地・丘陵等は重み付け要素にできるが、単一条件を必須化して「川がなければ必ず0」「海岸なら必ず大量」とはしない。地質をRimWorldが持たない部分は、マップSeed由来の決定論的な地域差で抽象化する。

Environment併用時は、Environmentが所有する地形情報を追加の重み付けに利用できるが、砂鉄Def・採取Job・供給保証はIronmakingが所有する。

### 6.2 ゲーム上の制約

- 砂鉄堆積は初期製鉄の主要原料だが、**全マップに十分量を保証しない**。立地差をゲームプレイに残す。
- 砂鉄が乏しいマップでも研究・セーブが詰まないよう、交易で砂鉄または一般鉄材を補完できる。
- 最初の砂鉄採取にIronmaking自身でしか生産できない鉄材を要求しない。
- v1では砂鉄混じり土砂、粗砂鉄、洗浄済み砂鉄等の複数中間アイテムを作らない。洗浄・選別を独立ゲームプレイにするだけの価値が生じた場合のみ追加する。
- 鉄穴流しは中世末に接点があるが、近世の大規模体系と強く結び付くため、v1の主要供給前提にはしない。将来追加する場合も中世末相当の限定的な採取拡張として扱い、高殿たたら・近世量産体系まで持ち込まない。
- 水車の存在だけを理由に製錬量を増やさない。水力を使う具体工程が確定した場合だけWaterworks等との任意互換を追加する。
- 既存セーブへの自動遡及生成はv1必須条件にしない。既存マップに砂鉄堆積がない場合でも交易等の代替経路を残し、遡及生成を実装する場合は別途安全性を検証する。

### 6.3 MOとの総供給量

**MO + Ironmakingだけでは** MO鉄鉱床・Mine Shaftを変更しない。これは独立Mod同士を素直に併用した状態とする。

**MO + Japanization + Ironmaking** では、JapanizationがMO側資源供給を再調整する。ここでの重要なバランス不変条件は、**砂鉄を追加した結果、初期～中期の利用可能鉄量が単純加算で大幅増加しないこと**である。

統合構成では:
- 砂鉄を日本式製鉄の主要自然資源にする。
- MO鉄鉱石は削除せず、副次的ルートとして残す。
- 地表鉄鉱床だけでなくMine Shaftの反復Recipeも同じ総供給量として扱う。
- Mine Shaftは砂鉄ルートを早期に無意味化する無制限バイパスにしない。まず研究位置・作業量・出力の調整を優先し、経路削除は最後の手段とする。
- 正確な比率は固定せず、テストでは「砂鉄が主要ルートとして実際に選ばれること」と「MO標準より鉄総量が不必要に膨張しないこと」を合否基準にする。

### 6.4 交易も含めた鉄供給設計

鉱床/Mine Shaftを減らすだけでは、交易による輸入鉄材で製鉄工程を迂回できる。**供給源は地表採掘・Mine Shaft・交易（商人/拠点）・開始備蓄・報酬等を通算して比較する。** 日本式製鉄の自給価値を残しつつ、国内製鉄以前の鉄器加工に必要な輸入鉄材は維持する。

| 交易対象 | 役割と方針 |
|---|---|
| 砂鉄 | Ironmaking所有。砂鉄が少ない/既存マップで採れない場合の補完。限定的な商人販売と買取を可能にするが、全商人の常設大量在庫にしない |
| 鉄塊 | 工程中間材。製品用途が確定するまで標準商人の大量品目にしない |
| Vanilla Steel / MO IronIngot | **製鉄未研究でも買える輸入鉄材**として維持。地元製鉄を恒久的に無意味化する安価・大量・確実な供給は避ける |
| MO IronOre | MOだけなら既存交易に介入しない。Japanization統合時に砂鉄と鉄鉱石の販売・購入量を合わせて監査 |
| AMJ木炭 / MO Coal | 地元炭焼きが基本、輸入は補完。MOは石炭/木炭の由来が同一Defのため厳密区分しない |
| 将来の良質鋼 | 消費先が成立するまで通常商人の大量在庫へ加えない |

**責務の分離**
- Vanilla + Ironmaking: 自身の砂鉄等の交易設定と適切な商人への限定的な販売・買取をIronmakingが所有。Vanilla全商人のSteel在庫を一括変更しない。
- MO + Ironmaking: Ironmakingは自分の資源の通常MO互換だけを所有し、MO既存の鉱床・Mine Shaft・鉄材交易在庫は変更しない。
- MO + Japanization: Ironmakingがない場合は、MO既存の輸入鉄材を含む実用的な供給経路を残す。
- MO + Japanization + Ironmaking: JapanizationがMO所有の**鉄関連TraderKindDef/StockGenerator**を条件付きで再調整し、MO採掘量と商人在庫を合算して砂鉄を主要ルートにする。

**検証条件**
- 研究前でも輸入鉄材が利用できる。逆に、安価な輸入だけで大規模製鉄需要を安定して満たせない。商人の在庫確率・補充/再訪・価格・運搬・銀の制約は実測する。
- プレイヤーが原料を売れることと商人が原料を**販売する**ことは別。販売用StockGeneratorと買取用StockGeneratorを混同しない。
- 砂鉄のThingCategory/TradeTagを広域販売カテゴリへ無条件登録して、意図しない全商人の大量在庫にしない。Vanilla/外部Modの通常交易をグローバルに削除・再構成しない。
- 砂鉄/木炭/鉄材の売買価格と製鉄Recipeの歩留まりから、無償増殖や無条件の売買裁定が成立しないか確認する。作業時間・調達/輸送コストも含む。数値は未確定。
- MOの金属チェーンOFF時に鉱床とMine ShaftがIronIngotを直接出力すること、**ON/OFF双方でMO深部資源からIronOre/IronIngotを採掘できるか**、`ResourcesRaw` が鉄鉱石・鉄インゴットへ到達すること、Soren TraderKindが本当に使われるかを確認する。Vanilla1.6/外部Faction商人は別証拠が得られるまで未監査とする。
- MOの金属チェーン設定ON/OFF、既存マップ、拠点交易・キャラバンを別々に確認。最終ロード後の生成在庫を検査する。

### 6.5 MO金属チェーン設定と外部商人の残余リスク

- **砂鉄優勢の参照バランスはMOの `metalChain` ON時。** OFF時は地表鉄鉱床とMine Shaftが鉄インゴットを直接産出するため、原料の鉄鉱石だけを減らしても製鉄を迂回できる。OFFは互換プロファイルとして維持し、Japanizationから黙ってONに変更しない。
- MO `DankPyon_IronIngot` は `ResourcesRaw` 直下、`DankPyon_IronOre` は子カテゴリ `DankPyon_RawOres` に所属する。したがってMOの明示インゴット販売のほか `ResourcesRaw` カテゴリ販売も最終在庫で検査する。
- 添付MO 1.6のSoren系商人Defはあるが同梱XMLで他の参照元は確認できない。活性化した商人としての頻度・総供給量を推定しない。
- Vanilla本体1.6の商人在庫XMLと外部Faction商人は未監査。Ironmaking/Japanizationの条件付きMO互換だけで「全世界の交易も砂鉄中心」と主張しない。必要なら別途World Rules等の明示的な世界全体の商人方針を検討する。
- Japanizationの実装所有正本: https://github.com/sucRo-RimWorld/Ancient-Medieval-Japan-Medieval-Overhaul-Japanization/blob/main/Docs/Research/MedievalOverhaulJapanizationIronSupplyAudit.md。価格・販売率・出現数の確定はロード後テスト待ち。

### 6.6 さらに残る鉄材経路：Vanilla鉱床と外部Mines、燃料交易

- MOの `vanillaMine` 設定がOFFのとき、`MOSetting_VanillaMineables.xml` はVanilla `MineableSteel` の出現頻度を0へ変更し、`PreciousLump` から除外する。ON側では同じ無効化をしない。**MO導入だけでVanilla Steel鉱床が必ず消えるとは限らない。**
- MO 1.6は `wexman.mines` 併用時、`Excavate_Steel` の出力を `DankPyon_IronOre` 10にする互換Patchを持つ。MO Mine Shaft以外の外部採掘経路が存在する可能性を評価に加える。
- MOの `woodChain` ON時は、Vanillaの部族/アウトランダーの一般物資キャラバンと訪問商人に `DankPyon_RawWood` 250～400を販売追加するPatchがある。**鉄材販売ではないが木炭・製鉄燃料の調達コストに影響する可能性**として扱う。
- 優先する設定テストは `metalChain` ON/OFF × `vanillaMine` ON/OFFの4構成。 `woodChain` ON/OFFは代表構成で燃料供給を比較し、`wexman.mines` は導入時だけ追加検証する。各設定を勝手に切り替えて恒久化しない。
- 土地、商人、研究、労働と燃料制約をそろえて、供給量を**最終的に使える一般鉄材の換算量と調達時間**で比較する。生砂鉄1、鉱石1、インゴット1を同価値で足さない。
- 詳細静的監査と検証条件の正本はJapanizationの `Docs/Research/MedievalOverhaulJapanizationIronSupplyAudit.md`。価格・供給率と最終Defの数値は未確定。
 

### 6.7 深部資源の潜在的な直接インゴット供給（静的監査）

添付MO 1.6の `Defs/ThingDefs_Items/Items_Resources.xml` では、**`DankPyon_IronOre` と `DankPyon_IronIngot` の両方**に次の深部資源フィールドが宣言されている。

| ThingDef | `deepCommonality` | `deepCountPerPortion` | `deepLumpSizeRange` |
|---|---:|---:|---|
| `DankPyon_IronOre` | 5 | 45 | 20～30 |
| `DankPyon_IronIngot` | 5 | 45 | 20～30 |

`MOSetting_MetalChain.xml` に、上記2種の深部資源パラメータをON/OFFで変更する操作は確認できない。**深部から鉄インゴットを直接採掘できる可能性が、metalChain ON構成にも残る**。ただし `deepCommonality` の宣言だけで最終の深部資源生成・掘削可否・採掘可能な総量を確定してはならない。RimWorld 1.6で実際に生成・採掘されるThingDefと研究/設定/Modの影響を、ロード後テストで検証する。

Japanization統合時の供給会計には、**地表鉱床・深部資源・MO Mine Shaft・外部採掘Mod・砂鉄堆積・商人・交易外の報酬/解体**を別々の列として含める。砂鉄とMO IronOreはそのままの個数で比較せず、精錬・歩留まり・燃料/労働/研究制約を経て取得可能な一般鉄材の量と、到達までの時間を比較する。研究前に交易で鉄器加工できる進行は維持し、数値調整は実測後に行う。

### 6.8 砂鉄堆積地点のMVP実装設計（仕様候補）

以下は **Ironmakingの専用リポジトリ分離前に行う実装方式比較・MVP候補** であり、ThingDef名・生成量・採取量・出現率の確定値ではない。

**表現方式:** `AMJ_IronSandDeposit`（仮称）を有限の自然Thingとして置き、採取したとき `AMJ_IronSand`（仮称）を取得する。採取地点を無限回の作業台として扱わず、残存量がなくなれば消滅する。最初はVanillaのmineable採取メカニクスを内部利用する案を優先する。鉱石という表示・硬い岩塊の外見に偽装せず、低い砂鉄堆積物の絵・説明へ統一する。鉱業スキル・作業分類を独自の「採砂」Jobへ置き換える必要性は、既存採取Jobでの操作感を検証してから判断する。Plant化による生育/枯死/繁殖や、無限Terrain採掘は採用しない。

**生成責務:** Ironmakingが自身のMapGenを所有する。EnvironmentやMOの存在でIronmakingの砂鉄生成クラス/資源Defを別物にしない。初稿は新規生成マップの陸上候補セルへ、河畔・海岸近傍・砂礫地等で重み付けした有限堆積を配置する。条件に適する地形がない場合も「全マップ完全保障」にはせず、稀少な土地では交易から製鉄原料を得られる。地質情報をVanillaが直接提供しない部分はSeed由来の決定論的な立地差として抽象化する。

**技術選定:** Vanilla標準のMineable scatterだけで河川沿い/海岸沿いのセル距離による重み付けが実現できるかを実装前に確認する。足りない場合は小さな専用GenStep（C#）を第一候補とし、土壌・河川・海岸・地形・既存建築を壊さず、**採砂物Thingの配置だけを行う**。大規模な地形置換、鉱脈生成全体の上書き、Environment必須化を避ける。生成順序は地形確定後とし、開始時建物・クエスト・河川通路・特殊マップ構造と干渉しないか実機で検証する。

**配置と有限性の不変条件**
- 水中セル・壁/建築物・プレイヤー初期施設・採取不能セルを埋めない。採取可能位置への到達性を検証する。
- 砂鉄生成と採取は通常のSteel・MO鉄鉱床・MO深部資源設定を変更しない。追加する鉄の総供給量はJapanization統合時に調整する。
- 砂鉄堆積は再成長・自然再補充・無限Bill・深部資源として勝手に複製しない。マップ内有限供給の上限は配置物の初期総埋蔵量で決まる。
- 同じSeed・条件・Mod構成での生成は安定する。Unity/RimWorldグローバル乱数状態を破壊しない方式を選ぶ。
- v1では既存マップへの自動遡及生成を必須化しない。途中導入時は砂鉄交易と既存一般鉄材の調達で遊べる。途中削除・再導入で既存Thingが孤立する危険は別テストとする。
- Steam向け仕様には「資源地点は新規マップで生成／既存マップへ自動追加しない」旨を、該当制限を実装確認してから明記する。

**交易の最低契約:** 砂鉄はIronmaking所有の明示的なStockGeneratorで適切な地上商人へ限定的に流す。資源カテゴリを `ResourcesRaw` へ安易に接続し、全商人の包括的在庫に自動混入させない。買えることと売れること、販売確率と買取可否を区別し、VanillaのSteel・MOのIronIngot在庫の既存設定をIronmaking単体で直接削らない。販売元の種類と具体的な数量・価格はRimWorld 1.6実機で調整する。

**実装直前の機械確認:** 砂鉄候補採取ThingのMineableデフォルト・工作業者・収穫時の出力/消失・絵の描画を最小マップで確認。テストマップを複数地形/Seedで反復生成し、全量採取で再出現しないこと、採取不能な孤立セルに置かれないこと、MOなし/MOありの同じAMJ ThingDefが維持されることを確認する。詳細な地形ごとの重み・個数はこのゲートを通過してから確定する。

### 6.9 MOゴーレム岩の大量鉄資源経路（静的監査）

MO本体の `DankPyon_GolemRock_Iron_MapGen` は鉱石450、`DankPyon_GolemRock_Iron_Incident` は鉱石1000をそれぞれ採掘産出として宣言する。前者は `GenStep_ScatterThings` と `MapCommonBase` へのMO Patchに接続し、後者は `DankPyon_GolemImpactor` 事件から参照される。MO金属チェーンOFF時は両者も鉄インゴット出力に切り替わる。**通常のMO鉱床40と同列のランダム鉱脈とは扱わない**。危険な幻想的イベント/生成との結び付きを含めた資源供給経路として、Japanizationが追加監査する。

日本化構成で幻想的ゴーレムを標準出現させるかは、JapanizationのPawn/Faction/生成・Incident全体の調整責務。採掘資源を減らすためだけにIronmakingがゴーレムを無効化しない。総鉄供給の計算では、イベント産出の数値を無条件に得られる確定収入として計上せず、発生頻度・入手危険・ロード後の挙動を確認する。


### 6.10 World Tech Level（任意推奨）による資源・交易制御

AMJ全体で推奨するWorld Tech LevelのMedieval設定は**IronmakingやJapanizationの必須依存ではない**。World Tech Levelは研究、Items（商人在庫）、Mineable Resources（鉱床）、Map Generation Stepsを別々にフィルタする。

World Tech Level 1.6の公開ソースでは、`Patch_StockGenerator` が `StockGenerator_Category` / `StockGenerator_MiscItems` / `StockGenerator_Tag` の技術レベル制限を変更する。一方、MOの鉄インゴット大量販売の `StockGenerator_SingleDef` は**そのPatchの対象外**。WTL導入だけでMO固定在庫が削減されると仮定しない。

Vanilla `DeepDrilling` 研究はIndustrialのため、WTL Medievalで研究フィルタONなら中世基準構成の標準取得経路にはなりにくい。既存研究・別Mod・フィルタOFF・旧セーブ等は別。**深部IronIngotの潜在経路は監査を残しつつ、基準構成では地表鉱床・MO Mine Shaft・MO商人・ゴーレム岩・砂鉄を先に検証する。**

Ironmaking独自の砂鉄 `ThingDef`、採取地点、研究とGenStepがWTLの対象時代から誤って排除されないようTechLevel・前提・生成結果をテストする。WTLを必須依存とせず、フィルタOFFでもIronmakingの仕様が成立することを確認する。

参照:
- https://github.com/m00nl1ght-dev/WorldTechLevel/blob/main/Sources/WorldTechLevel/Patches/Patch_StockGenerator.cs
- https://github.com/m00nl1ght-dev/WorldTechLevel/blob/main/Sources/WorldTechLevel/Patches/Patch_GenStep_ScatterLumpsMineable.cs
- https://github.com/m00nl1ght-dev/WorldTechLevel/blob/main/Sources/WorldTechLevel/Patches/Patch_MapGenerator.cs
- https://rimworldhub.com/wiki/thing/DeepDrilling?type=ResearchProjectDef

### 6.11 砂鉄交易の初期XML（未実機検証）

砂鉄の交易補完用として、`Patches/TradeIronSand.xml`でVanillaの`Caravan_Neolithic_BulkGoods`と`Caravan_Outlander_BulkGoods`の存在を条件確認し、**砂鉄だけ**の`StockGenerator_SingleDef`（販売）および`StockGenerator_BuySingleDef`（買取）を追加する。鉄インゴット/Steel/鉄鉱石や他資源のStockGeneratorは削除・置換しない。Vanilla Core 1.6の当該TraderKindDef実体およびキャラバン出現率はまだ未監査で、**取引可能なキャラバンが必ず訪れる保証はない**。実機で存在/生成/売買方向を確認し、必要なら同じ責務の範囲で拠点商人等を追加する。数量と売価は暫定。MO商人の既存IronIngot在庫はJapanizationの条件付き調整担当であり、このModから削減しない。

## 7. 添付MO 1.6実装監査

調査対象は添付のMO本体 `3219596926.zip`。以下はそのスナップショットのXML事実であり、最新Workshop全体やロード後の最終値を保証しない。

| 実ファイル（MOの1.6/以下） | 確認事実 / 設計への影響 |
|---|---|
| Defs/ProcessorDef/ProcessDef_CharcoalPile.xml | `DankPyon_WoodIntoCoal` はRawWoodカテゴリから `DankPyon_Coal` を出力。processDays=3、efficiency=2 |
| Defs/ThingDefs_Items/Items_Resources.xml | `DankPyon_Coal` は石炭として説明され、MO FuelValuePropertyのfuelValue=4を持つ。独立Charcoal Defを前提にできない。さらに `DankPyon_IronOre` と `DankPyon_IronIngot` の両方が深部資源設定 (commonality 5 / count 45 / lump 20～30) を持つため、**深部の直接鉄材供給**が潜在的な競合経路となる |
| Defs/ProcessorDef/ProcessDef_Smelter.xml | `DankPyon_SmeltingOre_Iron` はIronOre→IronIngot、`DankPyon_SmeltingOre_Steel` はIronIngot→Vanilla `Steel`。共通baseはprocessDays=0.24 |
| Defs/ThingDefs_Buildings/Production/Buildings_Processors.xml | `DankPyon_Smelter` はPF処理、Coal燃料、MO燃料保存・UIを利用。研究は `DankPyon_Steel`。建設にSteel80を要求し、AMJ最初の炉の代替にはしない |
| Defs/ResearchProjectDefs/ResearchProjects_Misc.xml | `DankPyon_Steel` はbaseCost=2000、Alchemy前提、Smithing hiddenPrerequisite |
| Patches/ToggleOptions/MOSetting_MetalChain.xml | 金属チェーン設定の切替で鉱物出力・設備・研究表示等が変わる。MO有無だけで互換判定を済ませない |
| Patches/Core/Add_FuelFilter.xml | 広い範囲のRefuelableへCoalやMO燃料カテゴリ・compを追加するPatchがある。AMJ炉にも適用されるか最終ロード後に確認する |
| Defs/TraderKindDefs/TraderKinds_Base_Medieval.xml | `DankPyon_Base_Medieval_Standard` は鉄インゴット500～800の販売StockGeneratorを直接定義。さらに `ResourcesRaw` カテゴリ生成があり、明示StockGeneratorだけ抑えても総在庫の再流入を確認する必要がある |
| Defs/TraderKindDefs/TraderKinds_Caravan_Medieval.xml | `DankPyon_Caravan_Medieval_BulkGoodsMerchant` は鉄インゴット100～200の販売StockGeneratorを直接定義 |
| Defs/TraderKindDefs/TraderKinds_Caravan_Soren.xml | `DankPyon_Caravan_Medieval_BulkGoodsMerchant_Soren` は鉄インゴット200～350の販売指定。鉱石の `StockGenerator_BuyTradeTag` とCoalの `StockGenerator_BuySingleDef` は買取指定であり販売在庫を意味しない。TradeTagの実一致は未検証 |
| Defs/ThingDefs_Items/Items_Resources.xml | `DankPyon_IronOre` の基礎MarketValue=0.4、`DankPyon_IronIngot` は1.5。売買の最終価格や実市場供給量は未検証 |
| Defs/ThingDefs_Buildings/Buildings_Natural.xml | `DankPyon_MineableIron` は `DankPyon_IronOre` を40産出、`mineableScatterCommonality=1`、鉱脈サイズ30~40。砂鉄を追加するだけでは鉄総供給量が増えるため、Japanization統合時の供給監査対象 |
| Defs/RecipeDefs/Recipes_MineShaft.xml / Defs/ThingDefs_Buildings/Production/Buildings_Production.xml | `DankPyon_MineShaft` は `DankPyon_Mining` 後に建築でき、鉄鉱石1個（workAmount 900）/5個（4500）の反復Recipeを持つ。地表鉱床だけを減らしても継続鉄供給が残るため、Japanization統合時はMine Shaftも同じ資源バランスとして扱う |

MOの木炭と石炭は当該実装では同じ出力Defになるため、公式互換が `DankPyon_Coal` を使う場合は由来を区別できない。木炭由来のみ許可するために全MO燃料体系を作り直すことは今回の前提にしない。**AMJ木炭Def自体はセーブ互換とStandaloneのため保持し、MO有効時はAMJ側の重複炭焼きRecipeを通常露出させず、MO CoalをIronmaking炉の標準燃料として受け入れる方向を第一候補とする。** 既存セーブ内のAMJ木炭は消費可能なまま残す。

MOの一般炉や燃料compをBaseで継承しない。PFを採るかは未確定。採用する場合はIronmaking自身の必要性に基づき直接依存宣言し、MOの推移的依存に頼らない。通常Bill方式と比較して決める。

資料識別:
- MO本体zip SHA-256: `6ed379d7c400db43b3af2a9a7fd6203f7f7e99ca1a670d36b0f73fd1adccc9e3`
- `2665554648.zip` は `Lucifel.MedievalOH.JPT`（日本語翻訳）で、本体資源の所有者ではない。
- `Defs.zip` は水利・衛生およびMO/DBH/PF向けPatchを含む補助資料。製鉄の主要Base依存をそこから導かない。
- `DBHforMedieval.dll` は本調査で逆コンパイルしていない。DLL内部挙動の確認済み・製鉄互換成功とは扱わない。
- 旧たたら製鉄、新1.6パッチ、Rice cultivating civilizationの実ファイルは添付されていない。前チャットのRecipe数量・完全動作・配布許諾の主張は、ここではソース監査済みの事実として採用しない。参考対象でありコード/XML/画像の転用許可を推定しない。

### VE系先行監査

Vanilla Expanded系では **Vanilla Factions Expanded - Medieval 2** を機能単位で再確認する。公開説明上はNeolithicとIndustrialの間を埋める広範な中世コンテンツであり、砂鉄採取 → 日本式製鉄炉 → 中世たたらという資源・製鉄進行の代替ではない。外部互換例から `VFEM2_SmithingAnvil` と `VFEM2_ForgeBellows` という鍛冶用Linkableの存在は確認できるため、将来の任意互換・設備補助の先行例にはできる。

結論は **前提採用しない / 実装参考 + 任意互換候補**。Ironmakingの主要ループを得るためにVFE Medieval 2を必須化せず、併用時にLinkable効果を安全に接続できる場合だけ互換Patchを検討する。

参考:
- https://steamcommunity.com/sharedfiles/filedetails/?id=3444347874
- https://github.com/Daria40K/Big-Little-Mod-Patch

## 8. 歴史資料と実装制限

設計根拠:
1. [広島県教育委員会「古墳時代の鉄をつくる」](https://www.pref.hiroshima.lg.jp/site/rekimin/tenji-tetu.html): 6世紀頃の炉、円筒・箱形、砂鉄と炭、鉄塊、復元実験。
2. [鉄の道文化圏「たたら製鉄の進歩」](https://tetsunomichi.gr.jp/history-and-tradition/tatara-history/part-1/): 輸入鉄による鉄器加工、古代炉の地域差、中世の大型化・防湿・保温、近世設備との区別。
3. [鉄の道文化圏「玉鋼と日本刀」](https://tetsunomichi.gr.jp/katana/): 玉鋼の呼称は後世だが、それ以前にも作刀用の和鋼が存在。

史実の炉形・燃料・工程からゲーム上の選択肢を設計するが、研究費やRecipe数量は史料からの直接換算ではない。高殿たたら、永代たたら、天秤鞴、近世完成型の本床釣・大鍛冶体系を標準研究の完成形に置かない。中世の炉床や防湿構造そのものまで一律に除外する意味ではない。

正式なアイテム説明は日本語を先に作成し、作者承認後に英訳する。銑の中世利用法・特殊鋼のラベル・送風設備型式は追加史料監査を要する。

## 9. 検証と次の実装単位

2026-10-10時点で、**砂鉄堆積採掘の第一段XML（About / finite IronSand deposit / GenStep / MapGenerator Patch）と静的テスト**を追加した。炭焼き・小型炉・鉄塊→一般鉄材Billの**開発用XML定義**も追加した。砂鉄の限定的なキャラバン販売/買取Patchは追加済み。独立研究・中上位炉・承認済画像はまだ未実装。Vanilla+MO双方の実機Recipe動作は未検証。RimWorld実機の最終Def、採掘可否、描画、マップ生成、互換動作は未検証であり配布可否を主張しない。

実装の最小単位は **有限砂鉄堆積 + 炭化 + 小型炉 + 鉄塊 + 一般鉄材への合流** とする。独自「鉄器加工」研究、銑、鉄滓、良質鋼、鉄穴流し、専用送風設備はMVPへ入れない。改良製鉄炉・中世たたらは、この最小ループの採取量・燃料量・作業量を実測してから追加する。新リポジトリの作成・公開はこの文書で実施済みとはしない。

実装時の自動検証:
- Vanilla + Ironmaking、MO + Ironmakingを常設。MOの金属チェーン設定ON/OFFを含める。
- Environment / Waterworksは対応機能を実装した段階で対象プロファイルを追加。不要な直積を必須にしない。
- Base未解決MO/PF/DBH参照0、任意Patch条件、重複素材・Recipeの標準露出を検証。
- 無鉄備蓄から炭化・小型炉へ到達可能、実採取・製錬・鍛錬Billの材料消費・出力・研究・WorkGiverを検証。
- 燃料0・停止・作業中断・再開・セーブ再ロードで無償出力や二重消費を防ぐ。
- 原料効率、燃料効率、作業量、設備投資、輸送負担を分け、小型炉=少量/低投資、改良炉=汎用、中世たたら=大口/高効率という操業規模差が成立するか比較。
- MO一般鉄材合流後もSteel研究を迂回しないこと、MO炉・既存燃料UI・他資源が維持されることを検証。
- `MO + Ironmaking` ではMO鉄鉱床/Mine Shaftが変更されないこと、`MO + Japanization + Ironmaking` では砂鉄が主要ルートとして成立しつつMO鉄鉱石が副次ルートとして残ることを、地表鉱床・Mine Shaft・交易を含む総供給量で比較する。
- 砂鉄の限定的な販売・買取、低砂鉄マップでの輸入救済、研究前の鉄材輸入、販売・買取のStockGeneratorの区別、MO商人の鉄インゴット在庫と `ResourcesRaw` 経由の再流入をLoaded Traderで自動監査。MO金属チェーンON/OFFを含め、安価な大量輸入だけで日本式製鉄が無意味にならないことを確認。
- 素材変換・溶解・再利用を接続する場合、循環して純増する経路を検査。
- 途中追加・削除・MO着脱を別ケースとして検証。Def差替えだけで安全移行を保証しない。
- Pickle / RimTest Redux優先。非対話・非表示実行で必要な描画経路を保ち、対象Mod由来ERRORで全体を失敗にする。

## 10. 実装移行ゲート（2026-10-10）

独立実装の必要性について、[比較証拠](Research/IronmakingEntryEvidence-20261010.md)と[判定JSON](Research/IronmakingEntryDecision.json)を作成し、現行1.6/旧版・VE/非VE・Vanilla/MO/AMJの違いを分けた。判定記録は`status: ready`、証拠SHA-256・必須比較8件/4系統の機械的な同等条件照合はPASS。**ProjectのPython検証器の実ファイルをローカル実行したという主張ではない。** 判定は独立Modを実装する合理性を認めるもので、実機動作・最終配布を承認したものではない。既存Mod比較の詳細は[IronmakingExistingModEntryAudit-20261010.md](Research/IronmakingExistingModEntryAudit-20261010.md)。

最初の研究用プローブ（5件静的PASS）から、本リポジトリの砂鉄採取第一段へ限定的に進めた。**実装済DefName/PackageId**は`AMJ_IronSand`、`AMJ_IronSandDeposit`、`AMJ_IronmakingMaterials`、`AMJ_ScatterIronSand`、`sucro.ancientmedievaljapan.ironmaking`。これらは今後の互換参照点だが、数値・見た目・生成分布は未確定。現行XMLの`mineableYield=40`、`countPer10kCellsRange=0.8~1.6`、`MarketValue=1`、商人在庫`countRange=10~30`は**試験用暫定値**で、史実・交易・実機バランスの採用値ではない。生成は単純な`GenStep_ScatterThings`で、河川/海岸/砂礫地の地域重みはまだ実装されていない。追加の開発用識別子は`AMJ_Charcoal`、`AMJ_IronBloom`、`AMJ_CharcoalKiln`、`AMJ_SmallIronFurnace`、`AMJ_BurnCharcoal`、`AMJ_SmeltIronSand`、`AMJ_ForgeIronBloom`。数量は`WoodLog 20→Charcoal 10`、`IronSand 40+Charcoal 60→IronBloom 10`、`IronBloom 10→Vanilla Steel 8`を**初期テスト値**として実装し、採用済み経済バランスとはしない。鍛錬にはVanillaの`FueledSmithy`/`ElectricSmithy`を使い、MOが存在する場合だけ`PatchOperationFindMod`で**`DankPyon_Anvil`＋`DankPyon_IronIngot 8`へ差し替える**。同じ条件で炉材料に`DankPyon_Coal`を追加する。MOのSteel研究短絡を避けるためVanilla Steelの出力をMOで残さない。製鉄炉・炭焼き設備はBill材料消費のみで`CompProperties_Refuelable`を持たず、二重燃料消費を避ける。MO時のAMJ木炭生産抑制は今後の検証対象で、現時点では残る。専用カテゴリ`AMJ_IronmakingMaterials`はVanilla側で既知の`Root`の直下に定義し、`ResourcesRaw`には接続しない。これにより一般商人の包括的`ResourcesRaw`経由への混入を避ける。初稿で使った`Resources`は確認できたカテゴリー一覧に存在しないため撤回した。依存Modは指定しない。使用しているVanilla画像は開発用代用で承認済み最終画像ではない。再現・静的検証手順は[IronSandStaticAudit](GoldenPaths/IronSandStaticAudit.md)に記録。今後もtopic branch→PR→チェック確認→mergeを使用する。

### 10.1 RimWorld実機／Pickleの自動E2E（2026-10-10、Vanilla 5/5 PASS・MO未実施）

[IronmakingPickleE2E](GoldenPaths/IronmakingPickleE2E.md)で実機起動ランナー、開発用PickleテストMod、Quickstartsによる生成・採掘・セーブの5シナリオを定義した。Vanilla単体とMO併用を**別々の独立Mod構成・SaveData**で検証する。実際の参照解決、Vanilla WorkGiverによる砂鉄採掘と有限性、Quickstart生成した砂鉄堆積、Pickle実セーブ／ロードを検証対象とし、MOプロファイルでは鉄塊からIronIngotへ合流する最終Recipeも照合する。2026-10-10、作者のWindows/RimWorld環境から報告されたVanilla実機ラン`b5a5596f84`は、**Pickle 5/5 PASS、skipped/flaky/error logs=0**。実行ログ上、隔離テスト用Modも削除された。ランの識別と報告原文は[Pickle実機検証記録](Testing/IronmakingPickleEvidence.md)に保存する。ゲーム実行は作者環境で行われ、このエージェントはローカル生成された`summary.json`や`Player.log`の実ファイルを直接再読取していない。MO併用ランは未報告、製錬Billのポーン作業、交易実在庫、実際の地理分布、導入後の旧セーブ、描画はまだこの5シナリオに含めない。シナリオPASSと未対象範囲を混同しない。
