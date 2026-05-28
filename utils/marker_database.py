#!/usr/bin/env python3
"""
Marker Database Management System

Handles local storage and management of marker information for the double-marking workflow.
Provides CRUD operations for marker data with JSON-based local storage.

Key Features:
- Local JSON storage (no external database costs)
- CRUD operations for markers
- Demo/Production mode support
- Real-time data synchronization
- Input validation and error handling

Author: Double-Marking System
Version: 2.0 - Enhanced Marker Management
"""

import json
import os
import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import pandas as pd

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MarkerDatabase:
    """
    Local marker database management with JSON storage.
    
    Provides complete marker CRUD operations for the double-marking workflow
    with support for both demo and production modes.
    """
    
    def __init__(self, db_file: str = "data/markers.json"):
        """Initialize marker database with local JSON storage."""
        self.db_file = db_file
        self.markers = {}
        self._ensure_data_directory()
        self._load_database()
        
        logger.info(f"Marker database initialized with {len(self.markers)} markers")
    
    def _ensure_data_directory(self):
        """Create data directory if it doesn't exist."""
        db_dir = os.path.dirname(self.db_file)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir)
            logger.info(f"Created data directory: {db_dir}")
    
    def _load_database(self):
        """Load marker database from JSON file."""
        try:
            if os.path.exists(self.db_file):
                with open(self.db_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.markers = data.get('markers', {})
                    logger.info(f"Loaded {len(self.markers)} markers from database")
            else:
                # Initialize with empty database and demo markers
                self.markers = {}
                self._create_demo_markers()
                self._save_database()
                logger.info("Created new marker database with demo markers")
                
        except Exception as e:
            logger.error(f"Error loading marker database: {str(e)}")
            self.markers = {}
            self._create_demo_markers()
    
    def _save_database(self):
        """Save marker database to JSON file."""
        try:
            data = {
                'markers': self.markers,
                'last_updated': datetime.now().isoformat(),
                'version': '2.0'
            }
            
            with open(self.db_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
            logger.info(f"Saved {len(self.markers)} markers to database")
            
        except Exception as e:
            logger.error(f"Error saving marker database: {str(e)}")
    
    def _create_demo_markers(self):
        """Create demo markers for testing purposes."""
        demo_markers = [
            {
                'marker_id': 'M001',
                'name': 'Dr. John Smith',
                'email': 'john.smith@keele.ac.uk',
                'department': 'Computer Science',
                'role': 'Senior Lecturer',
                'is_demo': True,
                'created_date': datetime.now().isoformat()
            },
            {
                'marker_id': 'M002', 
                'name': 'Dr. Jane Doe',
                'email': 'jane.doe@keele.ac.uk',
                'department': 'Computer Science',
                'role': 'Lecturer',
                'is_demo': True,
                'created_date': datetime.now().isoformat()
            },
            {
                'marker_id': 'M003',
                'name': 'Prof. Robert Wilson', 
                'email': 'robert.wilson@keele.ac.uk',
                'department': 'Computer Science',
                'role': 'Professor',
                'is_demo': True,
                'created_date': datetime.now().isoformat()
            },
            {
                'marker_id': 'M004',
                'name': 'Dr. Sarah Jones',
                'email': 'sarah.jones@keele.ac.uk', 
                'department': 'Computer Science',
                'role': 'Senior Lecturer',
                'is_demo': True,
                'created_date': datetime.now().isoformat()
            },
            {
                'marker_id': 'M005',
                'name': 'Dr. Michael Brown',
                'email': 'michael.brown@keele.ac.uk',
                'department': 'Computer Science', 
                'role': 'Lecturer',
                'is_demo': True,
                'created_date': datetime.now().isoformat()
            }
        ]
        
        for marker in demo_markers:
            self.markers[marker['marker_id']] = marker
            
        logger.info(f"Created {len(demo_markers)} demo markers")
    
    def generate_marker_id(self) -> str:
        """Generate next available marker ID."""
        existing_ids = [int(mid[1:]) for mid in self.markers.keys() if mid.startswith('M')]
        next_id = max(existing_ids) + 1 if existing_ids else 1
        return f"M{next_id:03d}"
    
    def add_marker(self, name: str, email: str, department: str = "Computer Science", 
                   role: str = "Lecturer", is_demo: bool = False) -> Tuple[bool, str]:
        """
        Add new marker to database.
        
        Args:
            name: Marker's full name
            email: Marker's email address
            department: Department name (default: Computer Science)
            role: Marker's role/position
            is_demo: Whether this is a demo marker
            
        Returns:
            Tuple of (success, message/marker_id)
        """
        try:
            # Validate inputs
            if not name.strip():
                return False, "Marker name cannot be empty"
            
            if not email.strip():
                return False, "Email address cannot be empty"
            
            if not '@' in email:
                return False, "Invalid email format"
            
            # Check for duplicate email
            for marker in self.markers.values():
                if marker['email'].lower() == email.lower():
                    return False, f"Email {email} already exists in database"
            
            # Generate new marker ID
            marker_id = self.generate_marker_id()
            
            # Create new marker
            new_marker = {
                'marker_id': marker_id,
                'name': name.strip(),
                'email': email.strip().lower(),
                'department': department.strip(),
                'role': role.strip(),
                'is_demo': is_demo,
                'created_date': datetime.now().isoformat(),
                'last_updated': datetime.now().isoformat()
            }
            
            # Add to database
            self.markers[marker_id] = new_marker
            self._save_database()
            
            logger.info(f"Added new marker: {marker_id} - {name} ({email})")
            return True, marker_id
            
        except Exception as e:
            logger.error(f"Error adding marker: {str(e)}")
            return False, f"Error adding marker: {str(e)}"
    
    def update_marker(self, marker_id: str, name: str = None, email: str = None, 
                      department: str = None, role: str = None) -> Tuple[bool, str]:
        """
        Update existing marker information.
        
        Args:
            marker_id: Marker ID to update
            name: New name (optional)
            email: New email (optional)
            department: New department (optional)
            role: New role (optional)
            
        Returns:
            Tuple of (success, message)
        """
        try:
            if marker_id not in self.markers:
                return False, f"Marker {marker_id} not found"
            
            marker = self.markers[marker_id]
            
            # Update provided fields
            if name is not None:
                if not name.strip():
                    return False, "Marker name cannot be empty"
                marker['name'] = name.strip()
            
            if email is not None:
                if not email.strip():
                    return False, "Email address cannot be empty"
                if not '@' in email:
                    return False, "Invalid email format"
                
                # Check for duplicate email (excluding current marker)
                for mid, m in self.markers.items():
                    if mid != marker_id and m['email'].lower() == email.lower():
                        return False, f"Email {email} already exists in database"
                
                marker['email'] = email.strip().lower()
            
            if department is not None:
                marker['department'] = department.strip()
            
            if role is not None:
                marker['role'] = role.strip()
            
            marker['last_updated'] = datetime.now().isoformat()
            
            self._save_database()
            
            logger.info(f"Updated marker: {marker_id} - {marker['name']}")
            return True, f"Marker {marker_id} updated successfully"
            
        except Exception as e:
            logger.error(f"Error updating marker {marker_id}: {str(e)}")
            return False, f"Error updating marker: {str(e)}"
    
    def delete_marker(self, marker_id: str) -> Tuple[bool, str]:
        """
        Delete marker from database.
        
        Args:
            marker_id: Marker ID to delete
            
        Returns:
            Tuple of (success, message)
        """
        try:
            if marker_id not in self.markers:
                return False, f"Marker {marker_id} not found"
            
            marker_name = self.markers[marker_id]['name']
            del self.markers[marker_id]
            self._save_database()
            
            logger.info(f"Deleted marker: {marker_id} - {marker_name}")
            return True, f"Marker {marker_name} deleted successfully"
            
        except Exception as e:
            logger.error(f"Error deleting marker {marker_id}: {str(e)}")
            return False, f"Error deleting marker: {str(e)}"
    
    def get_marker(self, marker_id: str) -> Optional[Dict]:
        """Get specific marker by ID."""
        return self.markers.get(marker_id)
    
    def get_all_markers(self, include_demo: bool = True) -> Dict[str, Dict]:
        """
        Get all markers from database.
        
        Args:
            include_demo: Whether to include demo markers
            
        Returns:
            Dictionary of all markers
        """
        if include_demo:
            return self.markers.copy()
        else:
            return {mid: marker for mid, marker in self.markers.items() 
                   if not marker.get('is_demo', False)}
    
    def get_markers_for_dropdown(self, include_demo: bool = True) -> List[str]:
        """
        Get formatted marker list for Streamlit dropdowns.
        
        Args:
            include_demo: Whether to include demo markers
            
        Returns:
            List of formatted strings: "Dr. John Smith (john.smith@keele.ac.uk)"
        """
        markers = self.get_all_markers(include_demo)
        dropdown_options = []
        
        for marker in markers.values():
            demo_label = " [DEMO]" if marker.get('is_demo', False) else ""
            option = f"{marker['name']} ({marker['email']}){demo_label}"
            dropdown_options.append(option)
        
        return sorted(dropdown_options)
    
    def parse_dropdown_selection(self, selection: str) -> Tuple[str, str, str]:
        """
        Parse dropdown selection to extract marker information.
        
        Args:
            selection: Dropdown selection string
            
        Returns:
            Tuple of (marker_id, name, email)
        """
        try:
            # Remove demo label if present
            clean_selection = selection.replace(" [DEMO]", "")
            
            # Extract name and email: "Dr. John Smith (john.smith@keele.ac.uk)"
            if "(" in clean_selection and ")" in clean_selection:
                name = clean_selection.split("(")[0].strip()
                email = clean_selection.split("(")[1].split(")")[0].strip()
                
                # Find marker ID by email
                for marker_id, marker in self.markers.items():
                    if marker['email'] == email:
                        return marker_id, name, email
                
                return "", name, email
            else:
                return "", clean_selection, ""
                
        except Exception as e:
            logger.error(f"Error parsing dropdown selection: {str(e)}")
            return "", selection, ""
    
    def get_marker_statistics(self) -> Dict:
        """Get database statistics."""
        total_markers = len(self.markers)
        demo_markers = len([m for m in self.markers.values() if m.get('is_demo', False)])
        production_markers = total_markers - demo_markers
        
        return {
            'total_markers': total_markers,
            'production_markers': production_markers,
            'demo_markers': demo_markers,
            'database_file': self.db_file,
            'last_updated': datetime.now().isoformat()
        }
    
    def export_to_dataframe(self) -> pd.DataFrame:
        """Export markers to pandas DataFrame."""
        markers_list = []
        for marker in self.markers.values():
            markers_list.append({
                'Marker ID': marker['marker_id'],
                'Name': marker['name'],
                'Email': marker['email'],
                'Department': marker['department'],
                'Role': marker['role'],
                'Type': 'Demo' if marker.get('is_demo', False) else 'Production',
                'Created': marker.get('created_date', 'Unknown'),
                'Last Updated': marker.get('last_updated', 'Unknown')
            })
        
        return pd.DataFrame(markers_list)
    
    def clear_demo_markers(self) -> Tuple[bool, str]:
        """Remove all demo markers from database."""
        try:
            demo_count = 0
            markers_to_delete = []
            
            for marker_id, marker in self.markers.items():
                if marker.get('is_demo', False):
                    markers_to_delete.append(marker_id)
                    demo_count += 1
            
            for marker_id in markers_to_delete:
                del self.markers[marker_id]
            
            self._save_database()
            
            logger.info(f"Cleared {demo_count} demo markers")
            return True, f"Removed {demo_count} demo markers"
            
        except Exception as e:
            logger.error(f"Error clearing demo markers: {str(e)}")
            return False, f"Error clearing demo markers: {str(e)}"

# Global instance for the application
marker_db = MarkerDatabase()