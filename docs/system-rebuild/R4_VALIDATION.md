# R4目录验证

45项目录/依赖/配方示例检查通过。

| 检查 | 结果 |
| --- | --- |
| recipe_ids_unique | 通过 |
| all_references_declared | 通过 |
| positive_counts_and_bounded_energy | 通过 |
| all_evidence_references_valid | 通过 |
| all_authored_products_reachable | 通过 |
| all_evidence_reachable | 通过 |
| manual_bootstrap_remains_without_tower | 通过 |
| separation_dry_budget_8 | 通过 |
| auto_separation_same_material_budget | 通过 |
| array_templates_declared | 通过 |
| ram_array_capacity | 通过 |
| storage_array_capacity | 通过 |
| control_state_capacity | 通过 |
| RAM_requires_manufactured_array | 通过 |
| storage_requires_manufactured_array | 通过 |
| controller_requires_real_program_region | 通过 |
| RAM_child_template_matches_capacity | 通过 |
| storage_child_template_matches_capacity | 通过 |
| all_67_legacy_items_mapped | 通过 |
| all_34_families_mapped | 通过 |
| all_15_stage_ids_retained | 通过 |
| source_README.md | 通过 |
| source_docs/DESIGN_HISTORY.md | 通过 |
| source_docs/Development_Log.md | 通过 |
| source_docs/INDEX.md | 通过 |
| source_docs/Kamaen_Info_Complex_Manufacturing_Process_Reference.md | 通过 |
| source_docs/Kamaen_Info_Computing_EDA_Design.md | 通过 |
| source_docs/Kamaen_Info_Core_Gameplay_Development_Plan.md | 通过 |
| source_docs/Kamaen_Info_GDD.md | 通过 |
| source_docs/Kamaen_Info_Hardware_TechTree_Design.md | 通过 |
| source_docs/Kamaen_Info_Information_System_Design.md | 通过 |
| source_docs/Kamaen_Info_Item_Block_Dictionary.md | 通过 |
| source_docs/Kamaen_Info_Optical_Computing_Design.md | 通过 |
| source_docs/Kamaen_Info_Resonance_Crystal_And_Early_Game_Design.md | 通过 |
| source_docs/Kamaen_Info_Stage_Content_Line.md | 通过 |
| source_docs/Kamaen_Info_TechTree_Plan.md | 通过 |
| source_docs/Kamaen_Runtime_Infrastructure/Complete_Path.md | 通过 |
| source_docs/Kamaen_Runtime_Infrastructure/MVP_Path.md | 通过 |
| source_docs/Kamaen_Runtime_Infrastructure/README.md | 通过 |
| source_count_18 | 通过 |
| bill_first_endpoint | 通过 |
| bill_first_board | 通过 |
| bill_two_racks | 通过 |
| B01_inference_32_fits | 通过 |
| B01_training_16_fits | 通过 |

验证能力：引用完整、名义材料/工位/证据自举可达、三套配方库存不为负及目标产出、指定内存预算、旧内容去向与18份旧源文件哈希。

范围限制：证据表的对象可达不证明实验已经通过；配方按名义成功路线且不模拟并行占用。目录去向不证明每个高阶模板已编码。未验证完整物理、真实配方质量、游戏渲染或实际游玩；模型/自动搭线行为另见专题中的验收表。
