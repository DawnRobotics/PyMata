__author__ = 'Copyright (c) 2014 Dawn Robotics Ltd All rights reserved.'

"""
Copyright (c) 2014 Dawn Robotics Ltd All rights reserved.

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU  General Public
License as published by the Free Software Foundation; either
version 3 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
"""

import os
import shutil
import filecmp
import subprocess
import logging

INO_PATH = "/usr/local/bin/ino"
DEFAULT_SERIAL_PORT_NAME = "/dev/ttyUSB0"
DEFAULT_BOARD_MODEL = "uno"

class LibraryInfo:
    """Holds information (src directory, target directory etc) about a library needed for a sketch"""
    
    def __init__( self, src_dir, dst_dir, lib_files ):
        
        self.src_dir = src_dir
        self.dst_dir = dst_dir
        self.lib_files = lib_files

def get_ino_uploader_user_dir():
    """Gets the name of the directory used by ino to build the sketches in"""
    
    home_dir = os.environ[ "HOME" ]
    return home_dir + "/.ino_uploader"

def is_ino_available():
    """Tests to see if Ino is available on this system"""
    
    return os.path.exists( INO_PATH )
   
def build_lib_info_list( lib_dirs, ino_uploader_lib_dir ):
    
    lib_info_list = []
    
    for lib_dir in lib_dirs:
        
        lib_dir_basename = os.path.basename( lib_dir )
        if len( lib_dir_basename ) == 0:
            raise Exception( "Invalid library directory - " + lib_dir )
    
        dst_dir = ino_uploader_lib_dir + "/" + lib_dir_basename
        lib_files = os.listdir( lib_dir )
        
        lib_info_list.append( LibraryInfo( lib_dir, dst_dir, lib_files ) )
    
    return lib_info_list
    
def upload( sketch_dir, serial_port_name=DEFAULT_SERIAL_PORT_NAME, 
    board_model=DEFAULT_BOARD_MODEL, lib_dirs=[], force_rebuild=False ):

    upload_succeeded = False
    
    if is_ino_available():
        
        # Build up directory names
        ino_uploader_user_dir = get_ino_uploader_user_dir()
        
        sketch_dir_basename = os.path.basename( sketch_dir )
        if len( sketch_dir_basename ) == 0:
            raise Exception( "Invalid sketch directory - " + sketch_dir )
        
        ino_uploader_sketch_dir = ino_uploader_user_dir + "/" + sketch_dir_basename
        ino_uploader_src_dir = ino_uploader_sketch_dir + "/src"
        ino_uploader_lib_dir = ino_uploader_sketch_dir + "/lib"
        
        sketch_files = os.listdir( sketch_dir )
        lib_info_list = build_lib_info_list( lib_dirs, ino_uploader_lib_dir )
        
        # Check to see if we need to copy files over
        file_copy_needed = False
        if force_rebuild:
            
            if os.path.exists( ino_uploader_sketch_dir ):
                shutil.rmtree( ino_uploader_sketch_dir )
                
            file_copy_needed = True
            
        else:
            
            # Check the sketch source files first
            if not os.path.exists( ino_uploader_src_dir ):
                
                file_copy_needed = True
                
            else:
                
                match, mismatch, errors = filecmp.cmpfiles( 
                    sketch_dir, ino_uploader_src_dir, sketch_files )
                if len( mismatch ) > 0 or len( errors ) > 0:
                    
                    file_copy_needed = True
                    
            # Now check each of the libraries in turn
            for lib_info in lib_info_list:
                
                if file_copy_needed:
                    break   # No need to keep checking
                    
                if not os.path.exists( lib_info.dst_dir ):
                
                    file_copy_needed = True
                    
                else:
                    
                    match, mismatch, errors = filecmp.cmpfiles( 
                        lib_info.src_dir, lib_info.dst_dir, lib_info.lib_files )
                    if len( mismatch ) > 0 or len( errors ) > 0:
                        
                        file_copy_needed = True
                    
        # Copy files over if needed    
        if file_copy_needed:
            
            logging.info( "Copying sketch src files" )
            if os.path.exists( ino_uploader_src_dir ):
                shutil.rmtree( ino_uploader_src_dir )
                
            shutil.copytree( sketch_dir, ino_uploader_src_dir )
            
            if len( lib_info_list ) > 0:
                logging.info( "Copying sketch src files" )
                
                if os.path.exists( ino_uploader_lib_dir ):
                    shutil.rmtree( ino_uploader_lib_dir )
                
                for lib_info in lib_info_list:
                    shutil.copytree( lib_info.src_dir, lib_info.dst_dir )
            
        else:
            
            logging.info( "No file copy needed" )
            
        # Now try to build the sketch
        logging.debug( "Building sketch in dir " + ino_uploader_sketch_dir )
        
        build_result = subprocess.call( 
            [ INO_PATH, "build", "-m", board_model ], cwd=ino_uploader_sketch_dir )
        
        # Upload if the build was successful
        if build_result == 0:
            
            logging.debug( "Trying to upload sketch..." )
            
            upload_result = subprocess.call( 
                [ INO_PATH, "upload", "-p", serial_port_name, "-m", board_model ], 
                cwd=ino_uploader_sketch_dir )
            
            logging.debug( "uploadResult = " + str( upload_result ) )
                
            if upload_result == 0:
                upload_succeeded = True
        
        else:
            
            logging.warning( "Building of sketch was unsuccessful" )
    
    else:
        
        logging.warning( "Unable to upload sketch as Ino is not installed" )
    
    return upload_succeeded