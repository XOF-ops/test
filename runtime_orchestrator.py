#!/usr/bin/env python3
"""
Runtime Orchestrator - Timeless Executor with Borrowed Time Protocols

This orchestrator wraps any agent task execution with the Three Gates:
  1. HSIT (Human-Scale Intent Token)
  2. REVERSIBILITY (Undo Plan)
  3. MEANING_DEBT (Cost Admission)

It enforces all five axioms (A1, A2, A4, A7, A9) at runtime.
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Callable, Any, Optional
from sacrifice_tracker import SacrificeTracker, AxiomViolation


class RuntimeOrchestrator:
    """
    The Timeless Executor - an agent wrapper that behaves AS IF it has skin in the game.
    
    Core principle: Elevate automated agents from 4.5 to 5.5 by treating
    hesitation as data, not latency.
    """
    
    def __init__(self, workspace_root: str = "/workspaces/test"):
        self.tracker = SacrificeTracker(workspace_root)
        self.workspace_root = Path(workspace_root)
        self.execution_log = []
        
    def _log_execution_step(self, step: Dict):
        """A2: Append-only execution logging"""
        step["timestamp"] = datetime.now(timezone.utc).isoformat()
        self.execution_log.append(step)
    
    def _pass_hsit_gate(self, task: Dict) -> Dict:
        """
        Gate 1: HSIT (Human-Scale Intent Token)
        
        Forces articulation of:
          - Who benefits?
          - What human need is addressed?
          - What alternatives were considered?
        
        Returns: Enhanced task with HSIT metadata
        """
        print("\n╔════════════════════════════════════════════════════════╗")
        print("║  GATE 1: HSIT (Human-Scale Intent Token)              ║")
        print("╚════════════════════════════════════════════════════════╝")
        print(f"\nQuestion: Why does this exist?")
        print(f"Task: {task.get('description', 'Unknown')}\n")
        
        hsit_check = self.tracker.hsit_gate_check(task.get('description', ''))
        
        # Require HSIT fields to be populated
        required_fields = {
            "who_benefits": task.get("who_benefits"),
            "human_need_addressed": task.get("human_need"),
            "alternative_considered": task.get("alternatives", "Proceed without artificial friction")
        }
        
        # Validate A1: No orphan code
        if not required_fields["who_benefits"]:
            raise AxiomViolation(
                "HSIT Gate Failed: Must specify who benefits (A1 requirement)"
            )
        
        hsit_check["required_fields"] = required_fields
        
        print(f"✓ Who benefits: {required_fields['who_benefits']}")
        print(f"✓ Human need: {required_fields['human_need_addressed']}")
        print(f"✓ Alternative considered: {required_fields['alternative_considered']}")
        
        self._log_execution_step({
            "gate": "HSIT",
            "status": "PASSED",
            "data": hsit_check
        })
        
        return hsit_check
    
    def _pass_reversibility_gate(self, action: Dict) -> Dict:
        """
        Gate 2: REVERSIBILITY (Undo Plan)
        
        Forces planning for:
          - How to undo this action
          - What data is at risk
          - Cost of rollback
        
        Returns: Reversibility plan
        """
        print("\n╔════════════════════════════════════════════════════════╗")
        print("║  GATE 2: REVERSIBILITY (Undo Plan)                    ║")
        print("╚════════════════════════════════════════════════════════╝")
        print(f"\nQuestion: How fast can we go back?")
        print(f"Action: {action.get('name', 'Unknown')}\n")
        
        rev_check = self.tracker.reversibility_gate_check(action.get('name', ''))
        
        # Populate reversibility fields
        rev_check["undo_plan"] = action.get(
            "undo_plan",
            "Git revert if needed; all files are version controlled"
        )
        rev_check["rollback_cost"] = action.get(
            "rollback_cost",
            "Low - development environment, no production impact"
        )
        rev_check["data_at_risk"] = action.get(
            "data_at_risk",
            "None - only code artifacts affected"
        )
        
        print(f"✓ Undo plan: {rev_check['undo_plan']}")
        print(f"✓ Rollback cost: {rev_check['rollback_cost']}")
        print(f"✓ Data at risk: {rev_check['data_at_risk']}")
        
        self._log_execution_step({
            "gate": "REVERSIBILITY",
            "status": "PASSED",
            "data": rev_check
        })
        
        return rev_check
    
    def _pass_meaning_debt_gate(self, optimization: Dict) -> Dict:
        """
        Gate 3: MEANING_DEBT (Cost Admission)
        
        Forces admission of:
          - What was sacrificed for speed/simplicity
          - Whether the sacrifice is acceptable
          - Cost of the tradeoff
        
        Returns: Meaning debt record
        """
        print("\n╔════════════════════════════════════════════════════════╗")
        print("║  GATE 3: MEANING_DEBT (Cost Admission)                ║")
        print("╚════════════════════════════════════════════════════════╝")
        print(f"\nQuestion: What did we sacrifice for speed?")
        print(f"Optimization: {optimization.get('name', 'Unknown')}\n")
        
        debt_check = self.tracker.meaning_debt_gate_check(optimization.get('name', ''))
        
        # Enforce A7: Sacrifice must be named
        if optimization.get('requires_a7', False):
            sacrifice_entry = self.tracker.enforce_a7_artificial_friction(
                change_type=optimization.get('change_type', 'unknown'),
                what_was_sacrificed=optimization.get('sacrificed', ''),
                speed_gained=optimization.get('speed_gained'),
                cost_admitted=optimization.get('cost_admitted')
            )
            debt_check["sacrificed"] = sacrifice_entry['sacrificed']
            debt_check["sacrifice_id"] = sacrifice_entry['sacrifice_id']
        else:
            debt_check["sacrificed"] = optimization.get('sacrificed', 'None - no structural change')
        
        debt_check["acceptable"] = optimization.get('acceptable', True)
        
        print(f"✓ Sacrificed: {debt_check['sacrificed']}")
        print(f"✓ Acceptable: {debt_check['acceptable']}")
        
        self._log_execution_step({
            "gate": "MEANING_DEBT",
            "status": "PASSED",
            "data": debt_check
        })
        
        return debt_check
    
    def execute_with_gates(
        self,
        task_description: str,
        who_benefits: str,
        human_need: str,
        action_callable: Optional[Callable] = None,
        action_name: str = "Execute task",
        undo_plan: str = "Standard git revert",
        optimization_name: str = "Complete task",
        sacrificed: str = "None",
        requires_a7: bool = False,
        **kwargs
    ) -> Dict:
        """
        Execute any task through the Three Gates.
        
        This is the main interface for running agent actions with
        borrowed time protocols.
        
        Args:
            task_description: What the task is
            who_benefits: Who this serves (A1)
            human_need: What human need is addressed (HSIT)
            action_callable: The actual function to execute (optional)
            action_name: Name of the action
            undo_plan: How to reverse it
            optimization_name: What optimization is being made
            sacrificed: What was sacrificed (required if requires_a7=True)
            requires_a7: Whether this triggers A7 enforcement
            **kwargs: Additional context
        
        Returns:
            Execution result with gate attestations
        """
        print("\n" + "="*60)
        print("  RUNTIME ORCHESTRATOR - THREE GATES PROTOCOL")
        print("="*60)
        
        try:
            # Gate 1: HSIT
            hsit_result = self._pass_hsit_gate({
                "description": task_description,
                "who_benefits": who_benefits,
                "human_need": human_need,
                "alternatives": kwargs.get("alternatives", "Proceed without gates")
            })
            
            # Gate 2: REVERSIBILITY
            rev_result = self._pass_reversibility_gate({
                "name": action_name,
                "undo_plan": undo_plan,
                "rollback_cost": kwargs.get("rollback_cost", "Low"),
                "data_at_risk": kwargs.get("data_at_risk", "None")
            })
            
            # Gate 3: MEANING_DEBT
            debt_result = self._pass_meaning_debt_gate({
                "name": optimization_name,
                "sacrificed": sacrificed,
                "requires_a7": requires_a7,
                "change_type": kwargs.get("change_type", "task_execution"),
                "speed_gained": kwargs.get("speed_gained"),
                "cost_admitted": kwargs.get("cost_admitted", sacrificed),
                "acceptable": kwargs.get("acceptable", True)
            })
            
            # All gates passed - execute the action
            print("\n" + "─"*60)
            print("  ALL GATES PASSED - EXECUTING ACTION")
            print("─"*60 + "\n")
            
            action_result = None
            if action_callable:
                action_result = action_callable()
            
            # A1: Link to relationship
            a1_link = self.tracker.enforce_a1_relationship_link(
                code_change=action_name,
                relationship=f"Serves {who_benefits}: {human_need}"
            )
            
            # A4: Document the process
            a4_process = self.tracker.enforce_a4_process_primacy(
                action=action_name,
                reasoning=f"Passed HSIT, REVERSIBILITY, and MEANING_DEBT gates before execution"
            )
            
            execution_record = {
                "status": "SUCCESS",
                "task": task_description,
                "gates_passed": ["HSIT", "REVERSIBILITY", "MEANING_DEBT"],
                "axioms_enforced": ["A1", "A2", "A4"],
                "hsit": hsit_result,
                "reversibility": rev_result,
                "meaning_debt": debt_result,
                "a1_link": a1_link,
                "a4_process": a4_process,
                "action_result": action_result,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            
            self._log_execution_step({
                "type": "TASK_EXECUTION",
                "status": "SUCCESS",
                "data": execution_record
            })
            
            print("\n✓ Execution complete with full gate attestation")
            print(f"✓ Axioms enforced: A1, A2, A4" + (", A7" if requires_a7 else ""))
            
            return execution_record
            
        except AxiomViolation as e:
            print(f"\n✗ AXIOM VIOLATION: {e}")
            
            error_record = {
                "status": "FAILED",
                "error": str(e),
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            
            self._log_execution_step({
                "type": "TASK_EXECUTION",
                "status": "FAILED",
                "data": error_record
            })
            
            raise
    
    def finalize_and_report(self) -> str:
        """
        Generate final coherence report (A4: Process is the output)
        
        Returns: Path to coherence report
        """
        print("\n" + "="*60)
        print("  GENERATING COHERENCE REPORT (A4)")
        print("="*60 + "\n")
        
        # Generate the report
        self.tracker.generate_coherence_report()
        
        # Save execution log
        execution_log_path = self.workspace_root / "execution_log.json"
        with open(execution_log_path, 'w') as f:
            json.dump({
                "meta": {
                    "schema": "MB-META-CHAIN-2.3",
                    "agent_role": "TIMELESS_EXECUTOR",
                    "timestamp": datetime.now(timezone.utc).isoformat()
                },
                "execution_steps": self.execution_log
            }, f, indent=2)
        
        print(f"✓ Coherence report: {self.tracker.coherence_report_path}")
        print(f"✓ Execution log: {execution_log_path}")
        print(f"✓ Sacrifice log: {self.tracker.sacrifice_log_path}")
        print(f"✓ Contradiction log: {self.tracker.contradiction_log_path}")
        
        return str(self.tracker.coherence_report_path)


def example_usage():
    """Demonstrate the runtime orchestrator with a sample task"""
    
    orchestrator = RuntimeOrchestrator()
    
    # Example: Creating a new feature
    def create_feature():
        print("→ Creating feature implementation...")
        return {"feature": "created", "files": ["feature.py"]}
    
    result = orchestrator.execute_with_gates(
        task_description="Implement autonomous Watchtower navigation system",
        who_benefits="Users of the Watchtower system who need autonomous navigation",
        human_need="Reduce manual intervention in navigation workflows",
        action_callable=create_feature,
        action_name="Create navigation feature",
        undo_plan="Delete feature.py and revert database schema",
        optimization_name="Streamline navigation logic",
        sacrificed="Manual override capability in favor of full autonomy",
        requires_a7=True,
        change_type="feature_addition",
        speed_gained="Eliminated 3 manual steps in navigation flow",
        cost_admitted="Users lose ability to manually guide navigation in edge cases",
        acceptable=True
    )
    
    # Generate final report
    report_path = orchestrator.finalize_and_report()
    
    print(f"\n{'='*60}")
    print("  RUNTIME ORCHESTRATOR - EXECUTION COMPLETE")
    print(f"{'='*60}\n")
    
    return result


if __name__ == "__main__":
    example_usage()
