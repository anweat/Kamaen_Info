# R1设计验证记录

运行方式：`python docs/system-rebuild/build_review.py`。仅生成R1图/覆盖/验证文件，不运行旧build_design.py，不回写原稿。

能力节点：78；主线：59；深化：19；里程碑：28；旧实体：164；阶段表独有：20。

| 检查 | 结果 |
| --- | --- |
| `all_nodes_reachable_and_no_dependency_cycle` | PASS |
| `all_28_milestones_have_core_content` | PASS |
| `ending_reachable_without_extensions_or_external_api` | PASS |
| `small_model_without_cluster` | PASS |
| `ordinary_power_before_crystal` | PASS |
| `local_scan_without_optics_or_cpu` | PASS |
| `electric_runtime_without_optical_branch` | PASS |
| `local_training_without_multisite_or_network` | PASS |
| `local_active_experiment_without_multisite` | PASS |
| `architecture_exploration_without_cluster_or_training` | PASS |
| `applications_have_local_non_ml_entry` | PASS |
| `late_branches_do_not_require_applications` | PASS |
| `electric_matrix_without_optical_matrix` | PASS |
| `optical_matrix_without_electric_matrix` | PASS |
| `hybrid_requires_both_matrices` | PASS |
| `first_cluster_without_optical_matrix_or_hybrid` | PASS |
| `initial_sky_without_quantum_or_cryo` | PASS |
| `material_windows_without_training_or_astronomy` | PASS |
| `lab_spectral_reference_without_training_or_cryo` | PASS |
| `quantum_lab_without_cryo_or_snspd` | PASS |
| `quantum_hybrid_requires_calibration_and_task_preparation` | PASS |
| `cross_requires_micro_and_cosmic_independently` | PASS |
| `initial_horizon_without_its_own_outputs` | PASS |
| `ending_requires_independent_return_anchor` | PASS |
| `all_three_modes_in_core_closure` | PASS |
| `ending_visits_all_core_capabilities` | PASS |
| `dictionary_all_164_rows_mapped` | PASS |
| `dictionary_unique_ids` | PASS |
| `no_mapping_for_nonexistent_dictionary_item` | PASS |
| `stage_only_20_rows_mapped` | PASS |
| `exact_stage_extra_mapping` | PASS |
| `18_original_sources_unchanged` | PASS |

## 验证的实际边界

- 可达/无环基于能力图，节点内精密/粗版部件与数量配方尚未完整验证。
- 可选分支删除实验验证依赖不阻塞，不能证明禁用相应内容后的所有经济平衡。
- 164+20是从源表逐行匹配，功能说明和修订做了人工核对；并非已注册或已实现内容。
- 本轮三项应用能力不计入旧实体覆盖数；其新增机体、移动储能、执行模块尚未并入R4数量目录，图可达不能替代物料/空间验算。
- L1仅修订凝聚态工作窗与实验室谱尺的模型前置，首批实验/仪器见LATE_L1_EXPERIMENTS_AND_INSTRUMENTS.md；新增组件的完整制程和数量没有由能力图验证。
- 18份原文SHA-256与源清单一致，未覆盖既有未提交修改。
- R1模型公式只完成适用域/数据来源设计；D1两个离线原型不能代表全模型已验证。
- 尚无Java更改、Gradle测试、实际试玩、时长平衡、多人/区块生命周期验证。

审核后的首批验证应优先做材料质量账、光电端到端成本、随机实验可辨识性和终局停机/返回状态机。
