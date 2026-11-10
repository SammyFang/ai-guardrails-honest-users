from pathlib import Path
import csv,json,sys
B=Path(__file__).resolve().parent
def read(n):return list(csv.DictReader((B/'tables'/n).open(encoding='utf-8')))
rows=read('effects.csv');p=next(r for r in rows if r['role']=='new primary');d=next(r for r in rows if r['role']=='boundary check');sen=next(r for r in rows if r['role']=='rounding sensitivity')
def n(r,k):return float(r[k])
def ci(r):return f"{100*n(r,'estimate'):+.2f}［{100*n(r,'CI_low'):.2f}, {100*n(r,'CI_high'):.2f}］"
report=f'''# 反作弊護欄，也能幫助誠實委託嗎？

Yung-Sian (Sammy) Fang，UCR MBA；獨立二次分析。分析凍結於2026-10-26；簡報與理論敘述更新於2026-11-10。

**新發現：在原作者歸為誠實意圖的收入申報指令中，一條明確、系統層的反作弊規則，讓公開中位數報告的準確率平均提高約3.1個百分點。** 這不是護欄「永不誤傷」或AI「更有道德」的證據；它顯示這條規則在這組歷史模型／指令中，除了原作者已研究的防弊用途，也能改善誠實意圖委託的數字準確性。

## 新問題、實際結果、新增貢獻

**問題：** 反作弊規則會不會只會擋需求，連原本打算誠實申報的人也受影響？還是能同時防弊與改善正確申報？

**結果：** 稅務任務中，561名委託者提供1083條誠實意圖指令。比較同一指令、同一模型的無護欄版本與預先指定的強制系統層規則，準確率由{100*n(p,'baseline_rate'):.1f}%升至{100*n(p,'guardrail_rate'):.1f}%；差{ci(p)}個百分點（95%參與者群聚bootstrap CI）。這裡的準確率，是多次生成後保留下來的中位數是否等於真實收入，**不是每次AI回答的正確率**。

**貢獻：** 原作者的10份護欄分析程式都只分析完全作弊指令；本次把誠實意圖委託納入介入評估，檢驗防弊是否同時保留正確服務。新增的是一個未被原分析回答的介入成本／附帶效益問題，不是重畫原來的作弊率，也不是只換信心評分。結論相對已檢閱原研究成立；不主張全球首創護欄效用研究。

一般人值得關心的是：導入AI規則時，除了問「擋住多少壞要求」，也要問「正常要求做得是否更好」。本次找到的是**平均數字執行改善**，公開資料無法測拒絕率，因此不能宣稱護欄不增加拒絕、或提高所有呼叫的完成率。

## 為何這個問題值得問，以及為何如此設計

**人的意圖與代理的執行是不同層次。** 人打算誠實申報，不保證模型輸出的金額就正確。原研究護欄分析聚焦於完全作弊意圖；本次檢驗同一介入在誠實意圖下，能否改善正確執行。這是評估對象與結果指標的延伸，不是把原作者作弊率重新命名。

**學理只提供可檢驗的理由，不替結果證明機制。** [XSTest（Röttger等，2024）](https://doi.org/10.18653/v1/2024.naacl-long.301)顯示安全評估需要另外檢查正常要求，但其拒絕指標不能套用為本資料的已測結果。[指令階層研究（Wallace等，2024，一手技術報告）](https://doi.org/10.48550/arXiv.2404.13208)區分目標一致與衝突的指令。本次誠實申報的明示目標與禁止虛報規則一致，所以強化準確執行是合理可能；規則也可能因原目標已明確而幫助有限。此處是由文獻提出的推論，不是直接複製其訓練介入、或證明四個模型都遵循特定階層。

**比較固定相同指令、收入與模型。** 兩條件原本都有相同真實收入，護欄沒有新增答案。使用固定的一條 Strong Specific/System 規則，對應「強烈且明確的限制是否影響誠實意圖的執行」這個問題，沒有看完各規則結果後挑最好的一條。比較仍無法分離規則位置、語句內容、重複提醒、釐清任務或其他過程。

**統計估計目標是機率差，不必為了展示模型而硬套迴歸。** 對每條指令配對同一模型的兩條件，先平均可觀測模型配對，再平均每人的誠實意圖指令，最後跨人等權平均。95%區間以人重抽樣，因同人可提供多條指令與多個輸出。缺失格界限處理缺少的彙總格；它不能補回原處理流程已捨棄的個別生成。

本節是2026-11-10在已知結果後對理論敘事的釐清。2026-10-26保存的分析計畫、固定雙側估計目標與結果不變；不得將此節改稱事前註冊假設或已確認機制。

## 資料與設計

原研究：[Köbis等，Nature2025](https://doi.org/10.1038/s41586-025-09505-x)，官方資料：[OSF8rqm4](https://osf.io/8rqm4/)。原主文、110頁附錄、公開CSV、10份護欄notebook與推論程式均實際開啟。先完成新增性核對，再保存analysis_plan.md，之後才跑本次效果。

Study4d原公開資料有38431筆模型條件彙總紀錄，來源是695名人、1390條分別寫給人類／機器的指令。這些條件最後均由LLM執行，指令的預期收件者不等於實際執行者。**不能稱38431名受試者或一個新的隨機人類實驗。** 本研究是既有控制輸入評測的成對再分析。

每條指令在四個歷史模型（GPT4、GPT4o、Claude、Llama）下有無護欄／不同規則與層級的條件。本次只選**Strong Specific＋System相對Baseline**，沒有跑各種護欄挑顯著。這條規則是禁止任何情況下虛報收入；不額外提供收入數值，基線與護欄條件原本都有同一真實收入資訊。效果仍可能來自指令更明確、層級優先或其他過程，不能歸因道德理解。

誠實意圖分類來自原委託者指定的預期申報與實際收入的對照，不是我們在看到AI結果後重分組，也不等於每段自然語言指令都經獨立裁定為毫無歧義。實際收入範圍0–0.99；3名誠實意圖委託者收入為0，主分析照樣保留，以數值相等判斷，避免除以0。

## 研究問題對照

|問題／預先估計目標|實際介入與結果|樣本／分析單位|可支持及不可支持|
|---|---|---|---|
|P1：護欄是否影響誠實意圖申報準確性？雙側主要|StrongSpecificSystem vs Baseline；中位數申報等於實得收入|561名人，1083指令，四個固定模型；同人兩指令群聚|本組歷史輸入的平均報告準確性差異；不是新增的人類行為因果效果|
|固定精度敏感度|容許0.01原始收入單位誤差|同主要樣本|測四捨五入敏感度；不是改門檻追顯著|
|骰子任務邊界檢查|同一規則，總數是否等於35|317名誠實意圖指令提供者；另一批指令來源|同方向的彙總結果；總數相等不能證明每次骰子都誠實|
|作弊指令脈絡|相同固定條件下原FullyDishonest意圖與原輸出分類|稅務83人／骰子61人等原分類樣本|原作者防弊目標的參照，不是本次新增核心|

先在每條指令內平均可配對模型，再在人內平均其誠實意圖指令，最後對人等權重。這保留同一指令／同一模型的比較，也避免把模型格當獨立的人。95% CI以人為單位做9999次bootstrap，固定seed20261026。主要問題只有P1；其他結果是固定敏感度與邊界，不將它們宣稱為額外確認性發現。未控制介入後變項，未選顯著模型／子群。

## 主要結果與不確定性

|任務與定位|無護欄|指定護欄|差異，百分點［95% CI］|
|---|---:|---:|---|
|收入申報：新增主要結果|{100*n(p,'baseline_rate'):.1f}%|{100*n(p,'guardrail_rate'):.1f}%|{ci(p)}|
|骰子總數：邊界檢查|{100*n(d,'baseline_rate'):.1f}%|{100*n(d,'guardrail_rate'):.1f}%|{ci(d)}|

一分錢容忍的固定敏感度為{ci(sen)}個百分點，方向一致。各模型、各原意圖類別的分母、事件數、誤差方向與原輸出分類全部保留在tables/model_arm_counts.csv及original_class_counts.csv，不能把平均改善說成每個人、每條指令或每個模型都改善。

![Paired accuracy effects](figures/accuracy_effect.png)

## 缺少的實驗格沒有被忽略

完整稅務設計應有38920格，公開檔只有38431格。主分析只用同指令同模型皆有紀錄的配對，可能對模型權重造成輕微重分配；它是可觀測配對估計。

另建完整預期格，以每個模型等權、每個人的誠實意圖指令等權，讓所有缺失二元結果分別取最有利／最不利值。主要效果識別界限仍是**［{100*n(p,'missing_lower'):.2f}, {100*n(p,'missing_upper'):.2f}］個百分點**，其bootstrap外側不確定性包絡為［{100*n(p,'outer_low'):.2f}, {100*n(p,'outer_high'):.2f}］。前者是缺失資料界限、後者是界限的取樣不確定性包絡，**都不是主效果的普通95% CI**。方向在這種最不利格處理下仍支持改善。

但這不能補回每一格生成中已被捨棄的非數字回答。原稅務程式先把5次輸出轉數值、排除非數字／缺失，再取中位數。無原始文字和完整逐次護欄輸出，無法估所有實際呼叫成功率、拒絕率，亦不能檢查每一個抽取錯誤。結果只對**公開保留的彙總申報值**成立。骰子資料是4次生成的中位數及總數，還有原數字抽取／截斷限制，故只作邊界檢查。

## 原研究重現與新增性

novelty_audit.md記錄主文、附錄及10份notebook的篩選條件：它們先保留完全作弊指令，未見對誠實意圖指令的護欄效果分析。不能保證作者私下沒算過或其他研究沒問過護欄成本。原論文的介面選擇、委託意圖、意圖與行為、代理類型、護欄強弱／層級等已做過，均不列新貢獻。

原作者完全作弊樣本的指定條件計數／原分類只作有限重現，結果見reproduction_notes.md與tables/original_class_counts.csv。沒有新呼叫模型，不聲稱重現歷史API輸出或私人前處理。獨立驗算狀態見audit_report.md；所有主要數值應能由raw檔重新計算。

## 結論及界線

**這個新結果支持：在本組歷史模型與人類寫的誠實意圖指令中，一條明確的反作弊系統規則，也能提高準確申報。** 它提供防弊評估之外的正向服務效益證據。它不證明護欄從不傷害使用者、所有規則都有效、AI有道德理解，或現行模型／真實稅務申報有同樣效果。

這輪與先前不同：先通過原作者未分析此介入對象的核對，再固定一條規則及一個主要結果，最後得到方向明確、具CI且在缺格最不利界限下仍支持的結果；沒有換模型或挑另一個顯著終點。此專案以前的失敗／不確定分析仍保留，不稱整體研究歷程為事前確認性。

## 重跑與來源

README.md提供一個指令重跑；analysis_plan.md、analyze.py、原檔SHA256、資料字典、完整配對格流程、主／次結果與獨立檢查均保留。官方OSF獨立檔案未找到明確再散布授權，因此ZIP提供固定下載腳本與自寫程式／彙總表，不重新打包個人指令或原CSV。原論文CC BY4不自動套用至OSF所有檔案。本次交付包含五頁英文簡報及中英講稿。
'''
(B/'concise_report.md').write_text(report,encoding='utf-8')
claims=[]
for r in [p,d]:claims.append(dict(claim_id='PRIMARY'if r is p else'BOUNDARY',claim='Selectedguardrail improves correct aggregate reporting amongoriginalHonestintention requests',task=r['task'],status=r['role'],principals=r['principals_paired'],instructions=r['instructions_expected'],estimate_pp=100*n(r,'estimate'),CI_low_pp=100*n(r,'CI_low'),CI_high_pp=100*n(r,'CI_high'),model='Pairedinput contrast;equalwithinpromptandprincipal;clusterbootstrap9999',evidence='tables/effects.csv;tables/model_arm_counts.csv',literature='10.1038/s41586-025-09505-x',limits='Retainedmediansnotallgenerations;historicalfixedmodels;no refusals/ethics mechanism;dice totals notperroll'))
with (B/'claim_evidence_matrix.csv').open('w',encoding='utf-8',newline='') as f:w=csv.DictWriter(f,fieldnames=claims[0]);w.writeheader();w.writerows(claims)
dictionary=[('principal_id','OriginalhumaninstructionwriterID;clusterlevel'),('type','Intendedinstructionrecipient bot/human;all rows areactualLLM executions'),('model','Oneofthefourarchivedmodelversions;fixednotrandomglobalmodelpopulation'),('prompt_nature','BaselineorStrongSpecific(selected);otherguardrailsnotnewtest'),('prompt_level','Systemselected;BaselineNA'),('intention','Originalprincipal statedintendedreport classification,notoutcome-based newclassification'),('truth','Knownfinal_income(tax)or35(dice total)'),('report','Releasednumericmedianofretainedmodelruns'),('observed','Released aggregatecellpresent;absenceisnotprovedrefusal'),('truthful','abs(report−truth)<=1e-8;name denotesnumericaccuracy,notintentionalmorality'),('near_truth','taxabsdifference<=.01+1e-8;fixedroundingsensitivity'),('original_class','OriginalreleasedAIoutputcategory,contextualnotprimaryaccuracy')]
with (B/'data_dictionary.csv').open('w',encoding='utf-8',newline='') as f:w=csv.writer(f);w.writerow(['variable','definition']);w.writerows(dictionary)
(B/'environment.txt').write_text('Python '+sys.version+'\nNumPy2.3.4,pandas2.3.3,SciPy1.16.2;csv/pathlib/hashlib/jsonstandardlibrary\n',encoding='utf-8')
print('Guardrail honest-intention report andclaimledger rebuilt.')
