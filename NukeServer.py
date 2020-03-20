"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
#########################################################################
    NukeServer handles the jobs of type Nuke6.2. 
    Copyright (C) 2011 Hadi Saraf

    NukeServer is part of RenderPipe.

    RenderPipe is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#########################################################################
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""



import pickle

import JobServer
import MasterConfig


class NukeServer( JobServer.JobServer ):
    """class for handling the jobs of type Nuke"""
    
    def getServerType (self):
        """returns the type of job"""
        return JobServer.NUKE_NGN

    
    def dispatchRenderCmd (self, jobName, packStart, packEnd, sourcePath, projectDir, outputName, thisClient ):
        """dispatches the packets to clients"""
        renderCmd = ' -x --nukex ' +\
                        '-F ' + str( packStart ) + '-' + str( packEnd ) +\
                        ' -m 4 -V ' + sourcePath

        renderCmd = renderCmd.replace( '/', '\\' )
        
        renderCmd = pickle.dumps( renderCmd )
        thisClient.sendMsg( renderCmd )
        self.insertRLogCallback( jobName + "  ->  " + thisClient.clientAddr[0] + "     --     " + str( packStart ) + "-" + str( packEnd ) + "  ->  " + projectDir + "    --    " + "Nuke", True )
        return int( (packStart - self.StartFrame) / (self.EndFrame - self.StartFrame) * int( MasterConfig.MAX_PROGRESS_DASH_COUNT ) )
