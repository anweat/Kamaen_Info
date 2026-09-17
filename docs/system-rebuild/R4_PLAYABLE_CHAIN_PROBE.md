# R4有限玩法链路验算

32项指定例子检查通过。脚本：[r4_playable_chain_probe.py](r4_playable_chain_probe.py)。

## 数值结果

| 示例 | 结果 |
| --- | --- |
| M01固定前向 | [0.6990000000000001, 0.195] |
| 两样本真实SGD，学习率0.01 | loss 0.002271625000 → 0.002186395509 |
| 58个梯度与中心差分比较 | 最大绝对差 2.45e-12 |
| 本地可用RAM | 3584 B；推理32/64=2536/4328 B；训练16/32=3384/5560 B |
| 两段圆弧的选中实际路线 | 长度 7.742477796；按1长度单位线材计8份；短路线碰维护区 |
| 2×2强度映射 | [0.6, 0.2] → [0.39999999999999997, 0.24000000000000005]；总量比η=0.8 |
| 终点控制 | 两批各一次炉请求；重复记录、无效输入与换批均不骗过连续窗 |

## 检查清单

| 检查 | 结果 |
| --- | --- |
| M01_forward_reference | 通过 |
| parameter_count_58 | 通过 |
| all_58_gradients_match_finite_difference | 通过 |
| one_SGD_step_decreases_example_loss | 通过 |
| input_initial_version_remains_reproducible | 通过 |
| inference32_fits_local_RAM | 通过 |
| inference64_exceeds_local_RAM | 通过 |
| training16_fits_local_RAM | 通过 |
| training32_exceeds_local_RAM | 通过 |
| two_remote_RAMs_do_not_rescue_local_batch64 | 通过 |
| replayed_sample_cannot_complete_three_frames | 通过 |
| three_new_frames_complete_endpoint | 通过 |
| invalid_sample_clears_ready | 通过 |
| batch_reset_precedes_first_new_sample | 通过 |
| one_furnace_request_per_batch | 通过 |
| inclusive_endpoint_limits | 通过 |
| late_old_batch_cannot_switch_active_batch | 通过 |
| short_route_collides_with_service_envelope | 通过 |
| long_route_clears_service_envelope | 通过 |
| long_route_meets_radius_and_leadout | 通过 |
| canonical_rounded_length | 通过 |
| chosen_route_has_material_budget | 通过 |
| optical_mapping_conserves_declared_loss | 通过 |
| example_mapping_has_no_negative_entries | 通过 |
| one_B01_rack_within_supply | 通过 |
| two_full_B01_boards_exceed_supply | 通过 |
| two_capped_boards_fit_supply | 通过 |
| B02_full_load_needs_capping | 通过 |
| split_hidden_activation_payload_bound | 通过 |
| RL_terminal_does_not_bootstrap_future_value | 通过 |
| RL_table_capacity | 通过 |
| gradient_reduction_weights_sample_counts | 通过 |

## 证据边界

- SGD前向、反传和更新在Python双精度中执行；游戏预算按f32计，未来实际f32内核应另用合理容差验证。一次下降不等于真实数据训练收敛。
- 两条预设平面路线使用明确直段/圆弧及保守包围盒检查；没有实现任意空间搜索、精确曲线碰撞、并发施工或Minecraft线路渲染。线材份数例不包含额外转换器；本例两端为同种铜包口。
- 内存、供给、通信是候选合同的数值反例，不模拟操作系统/总线或完整调度器。RL仅验证更新和终止语义，不声称完成环境训练。
- 材料可达、从零装配和旧稿覆盖另见[R4目录检查](R4_VALIDATION.md)。当前设计与旧局部物理推演均不替代后续实际试玩。
