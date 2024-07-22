import wx
import wx.grid
from uuid import uuid4
from threading import Thread
from time import sleep
from IPython import embed
from pprint import pformat

class Connections_Page(wx.Panel):
    def __init__(self, root, parent, frame):
        self._root=root
        self._frame=frame


        self._hosts={}
        self._hosts_uuid_mapping={}

        self._connections={}
        self._connections_uuid_mapping={}

        wx.Panel.__init__(self, parent)

        self._hosts_list=wx.ListCtrl(self, id=wx.ID_ANY, style=wx.LC_REPORT|wx.LC_SINGLE_SEL)
        self._hosts_list.InsertColumn(0, "IP Addr", width=200)

        self._metrics_list=wx.ListCtrl(self, id=wx.ID_ANY, style=wx.LC_REPORT|wx.LC_SINGLE_SEL)
        self._metrics_list.InsertColumn(0, "Connection Status", width=180)
        self._metrics_list.InsertColumn(1, "Local Address", width=300)
        self._metrics_list.InsertColumn(2, "Local Port", width=90)
        self._metrics_list.InsertColumn(3, "Remote Addr", width=180)
        self._metrics_list.InsertColumn(4, "Remote Addr Domain", width=250)
        self._metrics_list.InsertColumn(5, "Remote Port", width=90)


        self._geoip_textctrl=wx.TextCtrl(self, style= wx.TE_MULTILINE | wx.SUNKEN_BORDER)



        self._left_sizer=wx.BoxSizer(wx.VERTICAL)
        self._left_sizer.Add(self._hosts_list, 1, wx.EXPAND)

        self._right_sizer=wx.BoxSizer(wx.VERTICAL)
        self._right_sizer.Add(self._geoip_textctrl, 1, wx.EXPAND)

        self._middle_sizer=wx.BoxSizer(wx.VERTICAL)
        self._middle_sizer.Add(self._metrics_list, 1, wx.EXPAND)

        self._container_sizer=wx.BoxSizer(wx.HORIZONTAL)
        self._container_sizer.Add(self._left_sizer,1, wx.EXPAND)
        self._container_sizer.Add(self._middle_sizer, 3, wx.EXPAND)
        self._container_sizer.Add(self._right_sizer, 3, wx.EXPAND)

        self._main_sizer=wx.BoxSizer(wx.VERTICAL)
        self._main_sizer.Add(self._container_sizer, 1, wx.EXPAND)


        self.SetSizer(self._main_sizer)

        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self._on_host_select, self._hosts_list)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self._on_host_deselect, self._hosts_list)
        self.Bind(wx.EVT_LIST_COL_CLICK, self._on_sort, self._hosts_list)

        self.Bind(wx.EVT_LIST_COL_CLICK, self._on_sort, self._metrics_list)

        self.Bind(wx.EVT_LIST_COL_BEGIN_DRAG, self._veto_event, self._hosts_list)
        self.Bind(wx.EVT_LIST_COL_BEGIN_DRAG, self._veto_event, self._metrics_list)

        #self._frame._on_load.append(self._do_propagate_pixel_trackers)


    def _veto_event(self, event):
        event.Veto()

    def _on_sort(self, event):
        self.Layout()
        self.Update()

    def _do_update_geoip(self, event=None):


        indexes=list(self._hosts.keys())
        remote_addr=indexes[self._hosts_list.GetFocusedItem()]

        data=self._root._api_conn.get_geoip_data(remote_addr)
        data=pformat(data)
        self._geoip_textctrl.SetValue(data)

    def _do_propagate_hosts(self, event=None):    
        #self._hosts_list.DeleteAllItems()
        indexes=list(self._hosts.keys())


        for a in self._hosts:
            if self._hosts[a]['remote_addr']:
                list_item=self._hosts_list.GetItem(itemId=indexex.index(a), col=0).GetText()
            
            if list_item!=self._hosts[a]['remote_addr']:
                wx.CallAfter(
                    self._hosts_list.InsertItem,
                    indexes.index(a),
                    self._hosts[a]['remote_addr'],
                )

        wx.CallAfter(self.Layout)
        wx.CallAfter(self.Update)

    def _do_propagate_metrics(self):
        #embed()
        self._connections_uuid_mapping={}
        hosts_indexes=list(self._hosts.keys())
        metrics={}

        for connection in self._connections:
            if 'remote_addr' in self._connections[connection] and self._connections[connection]['remote_addr'] == hosts_indexes[self._hosts_list.GetFocusedItem()]:
                metrics[connection]=self._connections[connection]


        metrics_indexes=list(metrics.keys())
        wx.CallAfter(self._metrics_list.DeleteAllItems)

        for item in metrics:
            self._connections_uuid_mapping[item]=metrics_indexes.index(item)
            wx.CallAfter(
                self._metrics_list.InsertItem,
                metrics_indexes.index(item),
                metrics[item]['connection_status']
                )

            wx.CallAfter(
                self._metrics_list.SetItem,
                metrics_indexes.index(item),
                1,
                metrics[item]['local_addr']
                )

            wx.CallAfter(
                self._metrics_list.SetItem,
                metrics_indexes.index(item),
                2,
                str(metrics[item]['local_port'])
                )
        
            wx.CallAfter(
                self._metrics_list.SetItem,
                metrics_indexes.index(item),
                3,
                metrics[item]['remote_addr']
                )
        
            wx.CallAfter(
                self._metrics_list.SetItem,
                metrics_indexes.index(item),
                4,
                metrics[item]['remote_addr_domain'] if "remote_addr_domain" in metrics[item] else "---" 
                )

            wx.CallAfter(
                self._metrics_list.SetItem,
                metrics_indexes.index(item),
                5,
                str(metrics[item]['remote_port'])
                )
        

        wx.CallAfter(self.Layout)
        wx.CallAfter(self.Update)


    def _on_host_select(self, event):
        self._do_propagate_metrics()
        self._do_update_geoip()

    def _on_host_deselect(self,event):
        self._metrics_list.DeleteAllItems()

    def _blinker(self, connection_uuid):
        if connection_uuid in self._connections_uuid_mapping:
            wx.CallAfter(self._metrics_list.SetItemBackgroundColour, self._connections_uuid_mapping[connection_uuid], wx.Colour(0,150,0))
        
        if connection_uuid in self._hosts_uuid_mapping:
            print(self._hosts_uuid_mapping[connection_uuid])
            wx.CallAfter(self._hosts_list.SetItemBackgroundColour, self._hosts_uuid_mapping[connection_uuid], wx.Colour(0,150,0))

        wx.CallAfter(self.Layout)
        wx.CallAfter(self.Update)
        sleep(0.05)
        

        if connection_uuid in self._connections_uuid_mapping:
           wx.CallAfter(self._metrics_list.SetItemBackgroundColour, self._connections_uuid_mapping[connection_uuid], wx.Colour(30,30,30))
        
        if connection_uuid in self._hosts_uuid_mapping:
            wx.CallAfter(self._hosts_list.SetItemBackgroundColour, self._hosts_uuid_mapping[connection_uuid], wx.Colour(30,30,30))
        
        wx.CallAfter(self.Layout)
        wx.CallAfter(self.Update)

    def add_connection(self, connection):
        #print(connection)
        changed=False


        if 'remote_addr' in connection:


            if not connection['remote_addr'] in self._hosts:
                conn={
                "remote_addr": connection['remote_addr'],
                "remote_addr_domain": connection['remote_addr_domain'] if 'remote_addr_domain' in connection else "---",
                }

                self._hosts[connection['remote_addr']]=conn


                indexes=list(self._hosts.keys())
                self._hosts_uuid_mapping[connection['connection_uuid']]=indexes.index(connection['remote_addr'])


                wx.CallAfter(
                    self._hosts_list.InsertItem,
                    indexes.index(connection['remote_addr']),
                    connection['remote_addr'],
                )

                changed=True


        if connection['connection_status']== 'CONNECTION_ACCEPTED':
            self._connections[connection['connection_uuid']]=connection

        elif connection['connection_status']=='CONNECTION_OPEN':
            self._connections[connection['connection_uuid']]=connection

        elif connection['connection_status']=='CONNECTION_CLOSED':
            self._connections[connection['connection_uuid']]['connection_status']="CONNECTION_CLOSED"

        elif connection['connection_status']=='CONNECTION_DATA_TRANSMITING':
            if connection['connection_uuid'] in self._connections_uuid_mapping:
                t=Thread(
                    target=self._blinker, 
                    args=[connection['connection_uuid']]
                    )
                t.start()
                

        if changed:
            wx.CallAfter(self.Layout)
            wx.CallAfter(self.Update)




   
    