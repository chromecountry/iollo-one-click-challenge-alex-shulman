#!/usr/bin/env python3
"""
Analysis Pipeline Coordinator
Orchestrates the complete data analysis pipeline
"""
import subprocess
import sys
import os
from pathlib import Path
from datetime import datetime

def run_command(cmd, description, use_venv=True):
    """Run a command and handle errors"""
    print(f"\n🔄 {description}...")
    
    # Use virtual environment python if available and requested
    if use_venv and len(cmd) > 0 and cmd[0] == 'python3':
        script_dir = Path(__file__).parent
        venv_python = script_dir / 'venv' / 'bin' / 'python'
        if venv_python.exists():
            cmd[0] = str(venv_python)
    
    print(f"   Command: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(
            cmd, 
            capture_output=True, 
            text=True, 
            check=True
        )
        
        if result.stdout:
            print(f"   Output: {result.stdout.strip()}")
        
        print(f"   ✅ {description} completed successfully")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"   ❌ {description} failed!")
        print(f"   Error: {e.stderr.strip() if e.stderr else str(e)}")
        return False
    except FileNotFoundError as e:
        print(f"   ❌ {description} failed - file not found: {e}")
        return False

def check_prerequisites():
    """Check if all required components are available"""
    print("🔍 Checking prerequisites...")
    
    script_dir = Path(__file__).parent
    required_files = [
        'processor.py',
        'statistician.py', 
        'visualizer.py',
        'report_writer.py',
        'requirements.txt'
    ]
    
    missing_files = []
    for file in required_files:
        if not (script_dir / file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"   ❌ Missing required files: {', '.join(missing_files)}")
        return False
    
    print("   ✅ All required files present")
    
    # Check Python packages (basic check)
    try:
        import pandas
        import numpy  
        import matplotlib
        import seaborn
        print("   ✅ Core Python packages available")
        return True
    except ImportError as e:
        print(f"   ⚠️ Some Python packages missing: {e}")
        print("   📦 Run: pip install -r requirements.txt")
        return False

def create_sample_data():
    """Create sample data if none exists"""
    data_dir = Path(__file__).parent / 'data'
    sample_file = data_dir / 'sample.csv'
    
    if sample_file.exists():
        print(f"   ✅ Sample data already exists: {sample_file}")
        return str(sample_file)
    
    print("📊 Creating sample dataset...")
    data_dir.mkdir(exist_ok=True)
    
    # Create sample business data
    sample_data = """region,revenue,expenses,profit,employees,satisfaction,market_share
North,150000,120000,30000,45,4.2,0.15
South,180000,140000,40000,52,4.1,0.18
East,200000,160000,40000,60,4.3,0.20
West,175000,135000,40000,48,4.0,0.17
Central,160000,130000,30000,42,4.2,0.16
North,155000,125000,30000,47,4.1,0.15
South,185000,145000,40000,54,4.2,0.18
East,205000,165000,40000,62,4.4,0.21
West,170000,130000,40000,46,3.9,0.16
Central,165000,135000,30000,44,4.3,0.17"""
    
    with open(sample_file, 'w') as f:
        f.write(sample_data)
    
    print(f"   ✅ Created sample data: {sample_file}")
    return str(sample_file)

def setup_output_directory():
    """Create and setup output directory"""
    output_dir = Path(__file__).parent / 'outputs' / datetime.now().strftime('%Y%m%d_%H%M%S')
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"📁 Output directory: {output_dir}")
    return output_dir

def main():
    """Main coordination function"""
    print("🚀 Starting Data Analysis Pipeline")
    print(f"   Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Check prerequisites
    if not check_prerequisites():
        print("\n❌ Prerequisites check failed. Please install required packages.")
        sys.exit(1)
    
    # Setup paths
    script_dir = Path(__file__).parent
    input_data = create_sample_data()
    output_dir = setup_output_directory()
    
    # Define intermediate file paths
    processed_data = output_dir / 'processed_data.json'
    stats_results = output_dir / 'statistical_analysis.json'
    viz_dir = output_dir / 'visualizations'
    viz_catalog = viz_dir / 'visualization_catalog.json'
    final_report = output_dir / 'executive_report.md'
    
    print(f"\n📋 Pipeline Configuration:")
    print(f"   Input data: {input_data}")
    print(f"   Output directory: {output_dir}")
    print(f"   Working directory: {script_dir}")
    
    # Step 1: Data Processing
    success = run_command([
        'python3', str(script_dir / 'processor.py'),
        input_data,
        str(processed_data)
    ], "Data Processing")
    
    if not success:
        print("\n💥 Pipeline failed at data processing step")
        sys.exit(1)
    
    # Step 2: Statistical Analysis
    success = run_command([
        'python3', str(script_dir / 'statistician.py'),
        str(processed_data),
        str(stats_results)
    ], "Statistical Analysis")
    
    if not success:
        print("\n💥 Pipeline failed at statistical analysis step")
        sys.exit(1)
    
    # Step 3: Data Visualization
    success = run_command([
        'python3', str(script_dir / 'visualizer.py'),
        str(processed_data),
        str(stats_results),
        str(viz_dir)
    ], "Data Visualization")
    
    if not success:
        print("\n💥 Pipeline failed at visualization step")
        sys.exit(1)
    
    # Step 4: Report Generation
    success = run_command([
        'python3', str(script_dir / 'report_writer.py'),
        str(processed_data),
        str(stats_results),
        str(viz_catalog),
        str(final_report)
    ], "Report Generation")
    
    if not success:
        print("\n💥 Pipeline failed at report generation step")
        sys.exit(1)
    
    # Pipeline completed successfully
    print("\n" + "=" * 60)
    print("🎉 ANALYSIS PIPELINE COMPLETED SUCCESSFULLY!")
    print(f"\n📊 Results Summary:")
    print(f"   • Processed data: {processed_data}")
    print(f"   • Statistical analysis: {stats_results}")
    print(f"   • Visualizations: {viz_dir}")
    print(f"   • Executive report: {final_report}")
    print(f"\n📁 All outputs saved to: {output_dir}")
    print(f"\n🔍 Quick commands to view results:")
    print(f"   cat {final_report}")
    print(f"   ls -la {viz_dir}")
    print(f"   open {output_dir}  # (macOS) or explorer {output_dir}  # (Windows)")
    
    return str(output_dir)

if __name__ == "__main__":
    try:
        output_path = main()
        sys.exit(0)
    except KeyboardInterrupt:
        print("\n\n⚠️ Pipeline interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Pipeline failed with unexpected error: {e}")
        sys.exit(1)