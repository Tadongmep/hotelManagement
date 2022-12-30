/**
=========================================================
* Material Dashboard 2 React - v2.1.0
=========================================================

* Product Page: https://www.creative-tim.com/product/material-dashboard-react
* Copyright 2022 Creative Tim (https://www.creative-tim.com)

Coded by www.creative-tim.com

 =========================================================

* The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
*/

// @mui material components
import Grid from "@mui/material/Grid";
import Card from "@mui/material/Card";

// Material Dashboard 2 React components
import MDBox from "components/MDBox";
import MDTypography from "components/MDTypography";
import MDSnackbar from "components/MDSnackbar";

// Material Dashboard 2 React example components
import DashboardLayout from "examples/LayoutContainers/DashboardLayout";
import DashboardNavbar from "examples/Navbars/DashboardNavbar";
import Footer from "examples/Footer";
// import DataTable from "examples/Tables/DataTable";

// DevExtreme plugin
import DataGrid, {
  Column,
  Paging,
  // Selection,
  Editing,
  Popup,
  Form,
  FilterRow,
} from "devextreme-react/data-grid";
// import "devextreme-react/text-area";
import { Item } from "devextreme-react/form";
// import TextArea from "devextreme-react/text-area";
// Data
// import { customers } from "./data.js";
// import authorsTableData from "layouts/tables/data/authorsTableData";
// import projectsTableData from "layouts/tables/data/projectsTableData";

import { useState, useEffect } from "react";

function Tables() {
  // const { columns, rows } = authorsTableData();
  // const { columns: pColumns, rows: pRows } = projectsTableData();

  // components
  const [successSB, setSuccessSB] = useState(false);
  const closeSuccessSB = () => setSuccessSB(false);
  const [successMS, setSuccessMS] = useState("");

  const [errorSB, setErrorSB] = useState(false);
  const closeErrorSB = () => setErrorSB(false);
  const [errorMS, setErrorMS] = useState("");

  const renderSuccessSB = (
    <MDSnackbar
      color="success"
      icon="check"
      title="Material Dashboard"
      content={successMS}
      dateTime=""
      open={successSB}
      onClose={closeSuccessSB}
      close={closeSuccessSB}
      bgWhite
    />
  );

  const renderErrorSB = (
    <MDSnackbar
      color="error"
      icon="warning"
      title="Material Dashboard"
      content={errorMS}
      dateTime=""
      open={errorSB}
      onClose={closeErrorSB}
      close={closeErrorSB}
      bgWhite
    />
  );

  const dateFormat = { displayFormat: "dd/MM/yyyy" };
  // const timeFormat = { type: "time" };

  const detailInformation = (e) => {
    // console.log("ok men", e);
    if (e.rowType === "data") {
      e.component.editRow(e.rowIndex);
    }
  };

  if (localStorage.getItem("Position") === "admin") {
    // console.log("dang la admin");

    // for admin
    const [hotels, setHotels] = useState([]);
    const [rooms, setRooms] = useState([]);

    const addHotel = (e) => {
      // console.log("ok men", e);
      fetch(`/hotelRegister`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          name: e.data.name,
          address: e.data.address,
        }),
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.message === "hotel register successful") {
            setSuccessSB(true);
            setSuccessMS("Thêm khách sạn thành công");
          } else {
            setErrorSB(true);
            setErrorMS(data.message);
          }
        });
    };

    const deleteHotel = (e) => {
      // console.log("ok men", e.data.id);
      fetch(`/deleteHotel?id=${e.data.id}`, {
        method: "POST",
        // headers: {
        //   "Content-Type": "application/json",
        // },
        // body: JSON.stringify({
        //   name: e.data.name,
        //   address: e.data.address,
        // }),
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.message === "delete successful.") {
            setSuccessSB(true);
            setSuccessMS("Xóa khách sạn thành công");
          } else {
            setErrorSB(true);
            setErrorMS(data.message);
          }
        });
    };

    const updateHotel = (e) => {
      // console.log("ok men", e);
      // console.log("ok men", e.key.id);
      let newName = e.newData.name;
      let newAddress = e.newData.address;
      if (e.newData.name == null) {
        newName = e.oldData.name;
      }
      if (e.newData.address == null) {
        newAddress = e.oldData.address;
      }
      fetch(`/updateHotel?id=${e.key.id}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          name: newName,
          address: newAddress,
        }),
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.message === "update successful.") {
            setSuccessSB(true);
            setSuccessMS("Cập nhật khách sạn thành công");
          } else {
            setErrorSB(true);
            setErrorMS(data.message);
          }
        });
    };

    const addRoom = (e) => {
      // console.log("ok men", e);
      fetch(`/createRoom`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          belonging_to: e.data.belonging_to,
          kind_of_room: e.data.kind_of_room,
          room_name: e.data.room_name,
        }),
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.message === "room created.") {
            setSuccessSB(true);
            setSuccessMS("Thêm phòng thành công");
          } else {
            setErrorSB(true);
            setErrorMS(data.message);
          }
        });
    };

    const deleteRoom = (e) => {
      // console.log("ok men", e.data.id);
      fetch(`/deleteRoom?id=${e.data.id}`, {
        method: "POST",
        // headers: {
        //   "Content-Type": "application/json",
        // },
        // body: JSON.stringify({
        //   name: e.data.name,
        //   address: e.data.address,
        // }),
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.message === "delete successful.") {
            setSuccessSB(true);
            setSuccessMS("Xóa phòng thành công");
          } else {
            setErrorSB(true);
            setErrorMS(data.message);
          }
        });
    };

    const updateRoom = (e) => {
      // console.log("ok men", e);
      // console.log("ok men", e.key.id);
      let newBelongingTo = e.newData.belonging_to;
      let newKindOfRoom = e.newData.kind_of_room;
      let newRoomName = e.newData.room_name;
      if (e.newData.belonging_to == null) {
        newBelongingTo = e.oldData.belonging_to;
      }
      if (e.newData.kind_of_room == null) {
        newKindOfRoom = e.oldData.kind_of_room;
      }
      if (e.newData.room_name == null) {
        newRoomName = e.oldData.room_name;
      }
      fetch(`/updateRoom?id=${e.key.id}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          belonging_to: newBelongingTo,
          kind_of_room: newKindOfRoom,
          room_name: newRoomName,
        }),
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.message === "update successful.") {
            setSuccessSB(true);
            setSuccessMS("Cập nhật phòng thành công");
          } else {
            setErrorSB(true);
            setErrorMS(data.message);
          }
        });
    };

    useEffect(() => {
      fetch("/getHotel")
        .then((res) => res.json())
        .then((data) => {
          setHotels(data.message);
        });

      fetch("/getRoom")
        .then((res) => res.json())
        .then((data) => {
          setRooms(data.message);
        });
    }, []);
    return (
      <DashboardLayout>
        <DashboardNavbar />
        <MDBox pt={6} pb={3}>
          <Grid container spacing={6}>
            <Grid item xs={12}>
              <Card>
                <MDBox
                  mx={2}
                  mt={-3}
                  py={3}
                  px={2}
                  variant="gradient"
                  bgColor="info"
                  borderRadius="lg"
                  coloredShadow="info"
                >
                  <MDTypography variant="h6" color="white">
                    Danh Sách Khách Sạn
                  </MDTypography>
                </MDBox>
                <DataGrid
                  dataSource={hotels}
                  onRowClick={detailInformation}
                  onRowInserting={addHotel}
                  onRowRemoving={deleteHotel}
                  onRowUpdating={updateHotel}
                >
                  <Editing
                    mode="popup"
                    allowUpdating="true"
                    allowAdding="true"
                    allowDeleting="true"
                  >
                    <Popup title="Thông tin khách sạn" showTitle="true" width={650} height={250} />
                    <Form>
                      <Item itemType="group" colCount={1} colSpan={2}>
                        <Item dataField="name" />
                        <Item dataField="address" />
                        {/* <Item dataField="Prefix" />
                        <Item dataField="BirthDate" />
                        <Item dataField="Position" />
                        <Item dataField="HireDate" /> */}
                        {/* <Item
                          dataField="Notes"
                          editorType="dxTextArea"
                          colSpan={2}
                          editorOptions={notesEditorOptions}
                        /> */}
                      </Item>

                      {/* <Item itemType="group" caption="Home Address" colCount={2} colSpan={2}>
                        <Item dataField="StateID" />
                        <Item dataField="Address" />
                      </Item> */}
                    </Form>
                  </Editing>
                  {/* <Selection mode="single" /> */}
                  <Paging defaultPageSize={10} />
                  <Column dataField="id" caption="ID" dataType="string" />
                  <Column dataField="address" caption="Địa chỉ khách sạn" />
                  <Column dataField="name" caption="Tên khách sạn" />
                </DataGrid>
                {renderSuccessSB}
                {renderErrorSB}
                {/* <MDBox
                  mx={2}
                  mt={-3}
                  py={3}
                  px={2}
                  variant="gradient"
                  bgColor="info"
                  borderRadius="lg"
                  coloredShadow="info"
                >
                  <MDTypography variant="h6" color="white">
                    Authors Table
                  </MDTypography>
                </MDBox>
                <MDBox pt={3}>
                  <DataTable
                    table={{ columns, rows }}
                    isSorted={false}
                    entriesPerPage={false}
                    showTotalEntries={false}
                    noEndBorder
                  />
                </MDBox> */}
              </Card>
            </Grid>
            <Grid item xs={12}>
              <Card>
                <MDBox
                  mx={2}
                  mt={-3}
                  py={3}
                  px={2}
                  variant="gradient"
                  bgColor="info"
                  borderRadius="lg"
                  coloredShadow="info"
                >
                  <MDTypography variant="h6" color="white">
                    Danh Sách Phòng
                  </MDTypography>
                </MDBox>
                <DataGrid
                  dataSource={rooms}
                  onRowClick={detailInformation}
                  onRowInserting={addRoom}
                  onRowRemoving={deleteRoom}
                  onRowUpdating={updateRoom}
                >
                  {/* <Selection mode="single" /> */}
                  <Editing
                    mode="popup"
                    allowUpdating="true"
                    allowAdding="true"
                    allowDeleting="true"
                  >
                    <Popup title="Thông tin phòng" showTitle="true" width={650} height={300} />
                    <Form>
                      <Item itemType="group" colCount={1} colSpan={2}>
                        <Item dataField="belonging_to" />
                        <Item dataField="kind_of_room" />
                        <Item dataField="room_name" />
                        {/* <Item dataField="Prefix" />
                        <Item dataField="BirthDate" />
                        <Item dataField="Position" />
                        <Item dataField="HireDate" /> */}
                        {/* <Item
                          dataField="Notes"
                          editorType="dxTextArea"
                          colSpan={2}
                          editorOptions={notesEditorOptions}
                        /> */}
                      </Item>

                      {/* <Item itemType="group" caption="Home Address" colCount={2} colSpan={2}>
                        <Item dataField="StateID" />
                        <Item dataField="Address" />
                      </Item> */}
                    </Form>
                  </Editing>
                  <Paging defaultPageSize={10} />
                  <Column dataField="id" caption="ID" dataType="string" />
                  <Column dataField="belonging_to" caption="Thuộc khách sạn" />
                  <Column dataField="kind_of_room" caption="Loại phòng" />
                  <Column dataField="room_name" caption="Tên phòng" />
                </DataGrid>
                {/* <MDBox pt={3}>
                  <DataTable
                    table={{ columns: pColumns, rows: pRows }}
                    isSorted={false}
                    entriesPerPage={false}
                    showTotalEntries={false}
                    noEndBorder
                  />
                </MDBox> */}
              </Card>
            </Grid>
          </Grid>
        </MDBox>
        <Footer />
      </DashboardLayout>
    );
  }
  if (
    localStorage.getItem("Position") === "human resource" ||
    localStorage.getItem("Position") === "hotel manager"
  ) {
    // for human resource
    const [rosters, setRosters] = useState([]);
    const [laundryJobs, setLaundryJobs] = useState([]);
    const [gardeners, setGardeners] = useState([]);
    const [bellManJobs, setBellManJobs] = useState([]);
    const [linenRoomJobs, setLinenRoomJobs] = useState([]);
    const [housekeepingJobs, setHousekeepingJobs] = useState([]);
    const [waiterJobs, setWaiterJobs] = useState([]);

    // get data for table
    useEffect(() => {
      fetch("/getRosterInfor")
        .then((res) => res.json())
        .then((data) => {
          setRosters(data.message);
        });

      fetch("/getLaundryInfor")
        .then((res) => res.json())
        .then((data) => {
          setLaundryJobs(data.message);
        });

      fetch("/getGardenerInfor")
        .then((res) => res.json())
        .then((data) => {
          setGardeners(data.message);
        });

      fetch("/getBellManInfor")
        .then((res) => res.json())
        .then((data) => {
          setBellManJobs(data.message);
        });

      fetch("/getLinenRoomInfor")
        .then((res) => res.json())
        .then((data) => {
          setLinenRoomJobs(data.message);
        });

      fetch("/getHousekeepingInfor")
        .then((res) => res.json())
        .then((data) => {
          setHousekeepingJobs(data.message);
        });

      fetch("/getWaiterInfor")
        .then((res) => res.json())
        .then((data) => {
          setWaiterJobs(data.message);
        });
    }, []);

    const addRoster = (e) => {
      // console.log("ok men", e);
      fetch(`/createRoster`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          position: e.data.position,
          staff_id: e.data.staff_id,
          staff_name: e.data.staff_name,
          start_time: e.data.start_time,
          work_hour: e.data.work_hour,
          date: e.data.date,
          report: e.data.report,
        }),
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.message === "Create successful") {
            setSuccessSB(true);
            setSuccessMS("Tạo lịch phân công thành công");
          } else {
            setErrorSB(true);
            setErrorMS(data.message);
          }
        });
    };

    const deleteRoster = (e) => {
      fetch(`/deleteRoster?id=${e.data.id}`, {
        method: "POST",
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.message === "delete successful.") {
            setSuccessSB(true);
            setSuccessMS("Xóa thành công");
          } else {
            setErrorSB(true);
            setErrorMS(data.message);
          }
        });
    };

    const updateRoster = (e) => {
      let newPosition = e.newData.position;
      let newStaffId = e.newData.staff_id;
      let newStaffName = e.newData.staff_name;
      let newStartTime = e.newData.start_time;
      let newWorkHour = e.newData.work_hour;
      let newDate = e.newData.date;
      let newReport = e.newData.report;
      if (e.newData.position == null) {
        newPosition = e.oldData.position;
      }
      if (e.newData.staff_id == null) {
        newStaffId = e.oldData.staff_id;
      }
      if (e.newData.staff_name == null) {
        newStaffName = e.oldData.staff_name;
      }
      if (e.newData.start_time == null) {
        newStartTime = e.oldData.start_time;
      }
      if (e.newData.work_hour == null) {
        newWorkHour = e.oldData.work_hour;
      }
      if (e.newData.date == null) {
        newDate = e.oldData.date;
      }
      if (e.newData.report == null) {
        newReport = e.oldData.report;
      }
      fetch(`/updateRoster?id=${e.key.id}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          position: newPosition,
          staff_id: newStaffId,
          staff_name: newStaffName,
          start_time: newStartTime,
          work_hour: newWorkHour,
          date: newDate,
          report: newReport,
        }),
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.message === "update successful.") {
            setSuccessSB(true);
            setSuccessMS("Cập nhật thành công");
          } else {
            setErrorSB(true);
            setErrorMS(data.message);
          }
        });
    };

    const addLaundryJob = (e) => {
      // console.log("ok men", e);
      fetch(`/createLaundryJob`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          belonging_room_id: e.data.belonging_room_id,
          staff_execute_id: e.data.staff_execute_id,
          status: "Chưa xử lý",
          note: e.data.note,
        }),
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.message === "Create successful") {
            setSuccessSB(true);
            setSuccessMS("Tạo thành công");
          } else {
            setErrorSB(true);
            setErrorMS(data.message);
          }
        });
    };

    const deleteLaundryJob = (e) => {
      fetch(`/deleteLaundryJob?id=${e.data.id}`, {
        method: "POST",
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.message === "delete successful.") {
            setSuccessSB(true);
            setSuccessMS("Xóa thành công");
          } else {
            setErrorSB(true);
            setErrorMS(data.message);
          }
        });
    };

    const updateLaundryJob = (e) => {
      let newBelongingRoomId = e.newData.belonging_room_id;
      let newStatus = e.newData.status;
      let newStaffExecuteId = e.newData.staff_execute_id;
      let newNote = e.newData.note;
      if (e.newData.belonging_room_id == null) {
        newBelongingRoomId = e.oldData.belonging_room_id;
      }
      if (e.newData.status == null) {
        newStatus = e.oldData.status;
      }
      if (e.newData.staff_execute_id == null) {
        newStaffExecuteId = e.oldData.staff_execute_id;
      }
      if (e.newData.note == null) {
        newNote = e.oldData.note;
      }
      fetch(`/updateLaundryJob?id=${e.key.id}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          belonging_room_id: newBelongingRoomId,
          status: newStatus,
          staff_execute_id: newStaffExecuteId,
          note: newNote,
        }),
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.message === "update successful") {
            setSuccessSB(true);
            setSuccessMS("Cập nhật thành công");
          } else {
            setErrorSB(true);
            setErrorMS(data.message);
          }
        });
    };

    const addGadenerJob = (e) => {
      // console.log("ok men", e);
      fetch(`/createGardener`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          staff_execute_id: e.data.staff_execute_id,
          note: e.data.note,
        }),
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.message === "Create successful") {
            setSuccessSB(true);
            setSuccessMS("Tạo thành công");
          } else {
            setErrorSB(true);
            setErrorMS(data.message);
          }
        });
    };

    const deleteGadenerJob = (e) => {
      fetch(`/deleteGardenerJob?id=${e.data.id}`, {
        method: "POST",
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.message === "delete successful.") {
            setSuccessSB(true);
            setSuccessMS("Xóa thành công");
          } else {
            setErrorSB(true);
            setErrorMS(data.message);
          }
        });
    };

    const updateGadenerJob = (e) => {
      let newStaffExecuteId = e.newData.staff_execute_id;
      let newNote = e.newData.note;
      if (e.newData.staff_execute_id == null) {
        newStaffExecuteId = e.oldData.staff_execute_id;
      }
      if (e.newData.note == null) {
        newNote = e.oldData.note;
      }
      fetch(`/updateGardener?id=${e.key.id}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          staff_execute_id: newStaffExecuteId,
          note: newNote,
        }),
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.message === "update successful") {
            setSuccessSB(true);
            setSuccessMS("Cập nhật thành công");
          } else {
            setErrorSB(true);
            setErrorMS(data.message);
          }
        });
    };

    const addBellManJob = (e) => {
      // console.log("ok men", e);
      fetch(`/createBellManJob`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          belonging_room_id: e.data.belonging_room_id,
          status: e.data.status,
          staff_execute_id: e.data.staff_execute_id,
          note: e.data.note,
        }),
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.message === "Create successful") {
            setSuccessSB(true);
            setSuccessMS("Tạo lịch phân công thành công");
          } else {
            setErrorSB(true);
            setErrorMS(data.message);
          }
        });
    };

    const deleteBellManJob = (e) => {
      fetch(`/deleteBellManJob?id=${e.data.id}`, {
        method: "POST",
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.message === "delete successful.") {
            setSuccessSB(true);
            setSuccessMS("Xóa thành công");
          } else {
            setErrorSB(true);
            setErrorMS(data.message);
          }
        });
    };

    const updateBellManJob = (e) => {
      let newBelongingRoomId = e.newData.belonging_room_id;
      let newStatus = e.newData.status;
      let newStaffExecuteId = e.newData.staff_execute_id;
      let newNote = e.newData.note;
      if (e.newData.belonging_room_id == null) {
        newBelongingRoomId = e.oldData.belonging_room_id;
      }
      if (e.newData.status == null) {
        newStatus = e.oldData.status;
      }
      if (e.newData.staff_execute_id == null) {
        newStaffExecuteId = e.oldData.staff_execute_id;
      }
      if (e.newData.note == null) {
        newNote = e.oldData.note;
      }
      fetch(`/updateBellManJob?id=${e.key.id}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          belonging_room_id: newBelongingRoomId,
          status: newStatus,
          staff_execute_id: newStaffExecuteId,
          note: newNote,
        }),
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.message === "update successful") {
            setSuccessSB(true);
            setSuccessMS("Cập nhật thành công");
          } else {
            setErrorSB(true);
            setErrorMS(data.message);
          }
        });
    };

    const addLinenRoomJob = (e) => {
      // console.log("ok men", e);
      fetch(`/createLinenRoomJob`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          belonging_room_id: e.data.belonging_room_id,
          status: e.data.status,
          staff_execute_id: e.data.staff_execute_id,
          staff_laundry_id: e.data.staff_laundry_id,
          note: e.data.note,
        }),
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.message === "Create successful") {
            setSuccessSB(true);
            setSuccessMS("Tạo thành công");
          } else {
            setErrorSB(true);
            setErrorMS(data.message);
          }
        });
    };

    const deleteLinenRoomJob = (e) => {
      fetch(`/deleteLinenRoomJob?id=${e.data.id}`, {
        method: "POST",
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.message === "delete successful.") {
            setSuccessSB(true);
            setSuccessMS("Xóa thành công");
          } else {
            setErrorSB(true);
            setErrorMS(data.message);
          }
        });
    };

    const updateLinenRoomJob = (e) => {
      let newBelongingRoomId = e.newData.belonging_room_id;
      let newStatus = e.newData.status;
      let newStaffExecuteId = e.newData.staff_execute_id;
      let newNote = e.newData.note;
      if (e.newData.belonging_room_id == null) {
        newBelongingRoomId = e.oldData.belonging_room_id;
      }
      if (e.newData.status == null) {
        newStatus = e.oldData.status;
      }
      if (e.newData.staff_execute_id == null) {
        newStaffExecuteId = e.oldData.staff_execute_id;
      }
      if (e.newData.note == null) {
        newNote = e.oldData.note;
      }
      fetch(`/updateLinenRoomJob?id=${e.key.id}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          belonging_room_id: newBelongingRoomId,
          status: newStatus,
          staff_execute_id: newStaffExecuteId,
          note: newNote,
        }),
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.message === "update successful.") {
            setSuccessSB(true);
            setSuccessMS("Cập nhật thành công");
          } else {
            setErrorSB(true);
            setErrorMS(data.message);
          }
        });
    };

    const addHousekeepingJobs = (e) => {
      // console.log("ok men", e);
      fetch(`/createHousekeepingJob`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          belonging_room_id: e.data.belonging_room_id,
          status: e.data.status,
          staff_execute_id: e.data.staff_execute_id,
          note: e.data.note,
        }),
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.message === "Create successful") {
            setSuccessSB(true);
            setSuccessMS("Tạo thành công");
          } else {
            setErrorSB(true);
            setErrorMS(data.message);
          }
        });
    };

    const deleteHousekeepingJobs = (e) => {
      fetch(`/deleteHousekeepingJob?id=${e.data.id}`, {
        method: "POST",
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.message === "delete successful.") {
            setSuccessSB(true);
            setSuccessMS("Xóa thành công");
          } else {
            setErrorSB(true);
            setErrorMS(data.message);
          }
        });
    };

    const updateHousekeepingJobs = (e) => {
      let newBelongingRoomId = e.newData.belonging_room_id;
      let newStatus = e.newData.status;
      let newStaffExecuteId = e.newData.staff_execute_id;
      let newNote = e.newData.note;
      if (e.newData.belonging_room_id == null) {
        newBelongingRoomId = e.oldData.belonging_room_id;
      }
      if (e.newData.status == null) {
        newStatus = e.oldData.status;
      }
      if (e.newData.staff_execute_id == null) {
        newStaffExecuteId = e.oldData.staff_execute_id;
      }
      if (e.newData.note == null) {
        newNote = e.oldData.note;
      }
      fetch(`/updateHousekeepingJob?id=${e.key.id}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          belonging_room_id: newBelongingRoomId,
          status: newStatus,
          staff_execute_id: newStaffExecuteId,
          note: newNote,
        }),
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.message === "update successful") {
            setSuccessSB(true);
            setSuccessMS("Cập nhật thành công");
          } else {
            setErrorSB(true);
            setErrorMS(data.message);
          }
        });
    };

    const addWaiterJobs = (e) => {
      // console.log("ok men", e);
      fetch(`/createWaiterJob`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          belonging_room_id: e.data.belonging_room_id,
          status: e.data.status,
          staff_execute_id: e.data.staff_execute_id,
          note: e.data.note,
        }),
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.message === "Create successful") {
            setSuccessSB(true);
            setSuccessMS("Tạo thành công");
          } else {
            setErrorSB(true);
            setErrorMS(data.message);
          }
        });
    };

    const deleteWaiterJobs = (e) => {
      fetch(`/deleteWaiterJob?id=${e.data.id}`, {
        method: "POST",
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.message === "delete successful.") {
            setSuccessSB(true);
            setSuccessMS("Xóa thành công");
          } else {
            setErrorSB(true);
            setErrorMS(data.message);
          }
        });
    };

    const updateWaiterJobs = (e) => {
      let newBelongingRoomId = e.newData.belonging_room_id;
      let newStatus = e.newData.status;
      let newStaffExecuteId = e.newData.staff_execute_id;
      let newNote = e.newData.note;
      if (e.newData.belonging_room_id == null) {
        newBelongingRoomId = e.oldData.belonging_room_id;
      }
      if (e.newData.status == null) {
        newStatus = e.oldData.status;
      }
      if (e.newData.staff_execute_id == null) {
        newStaffExecuteId = e.oldData.staff_execute_id;
      }
      if (e.newData.note == null) {
        newNote = e.oldData.note;
      }
      fetch(`/updateWaiterJob?id=${e.key.id}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          belonging_room_id: newBelongingRoomId,
          status: newStatus,
          staff_execute_id: newStaffExecuteId,
          note: newNote,
        }),
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.message === "update successful") {
            setSuccessSB(true);
            setSuccessMS("Cập nhật thành công");
          } else {
            setErrorSB(true);
            setErrorMS(data.message);
          }
        });
    };

    return (
      <DashboardLayout>
        <DashboardNavbar />
        <MDBox pt={6} pb={3}>
          <Grid container spacing={6}>
            <Grid item xs={12}>
              <Card>
                <MDBox
                  mx={2}
                  mt={-3}
                  py={3}
                  px={2}
                  variant="gradient"
                  bgColor="info"
                  borderRadius="lg"
                  coloredShadow="info"
                >
                  <MDTypography variant="h6" color="white">
                    Bảng Phân Công Công Việc Cho Nhân Viên
                  </MDTypography>
                </MDBox>
                <DataGrid
                  dataSource={rosters}
                  onRowClick={detailInformation}
                  onRowInserting={addRoster}
                  onRowRemoving={deleteRoster}
                  onRowUpdating={updateRoster}
                >
                  <FilterRow visible="true" />
                  <Editing
                    mode="popup"
                    allowUpdating="true"
                    allowAdding="true"
                    allowDeleting="true"
                  >
                    <Popup title="Thông tin phân công" showTitle="true" width={650} height={510} />
                    <Form>
                      <Item itemType="group" colCount={1} colSpan={2}>
                        <Item dataField="position" />
                        <Item dataField="staff_id" />
                        <Item dataField="staff_name" />
                        <Item dataField="start_time" />
                        <Item dataField="work_hour" />
                        <Item dataField="date" editorOptions={dateFormat} />
                        <Item dataField="report" />
                      </Item>
                    </Form>
                  </Editing>
                  <Paging defaultPageSize={10} />
                  <Column dataField="id" caption="ID" dataType="string" />
                  <Column dataField="position" caption="Chức vụ" />
                  <Column dataField="staff_id" caption="ID nhân viên" />
                  <Column dataField="staff_name" caption="Tên nhân viên" />
                  <Column dataField="start_time" caption="Giờ bắt đầu ca" />
                  <Column dataField="work_hour" caption="Số giờ làm việc" />
                  <Column dataField="date" caption="Ngày phân công" />
                  <Column dataField="report" caption="Ghi chú" />
                </DataGrid>
                {renderSuccessSB}
                {renderErrorSB}
              </Card>
            </Grid>
            <Grid item xs={12}>
              <Card>
                <MDBox
                  mx={2}
                  mt={-3}
                  py={3}
                  px={2}
                  variant="gradient"
                  bgColor="info"
                  borderRadius="lg"
                  coloredShadow="info"
                >
                  <MDTypography variant="h6" color="white">
                    Danh Sách Dich Vụ Giặt Là
                  </MDTypography>
                </MDBox>
                <DataGrid
                  dataSource={laundryJobs}
                  onRowClick={detailInformation}
                  onRowInserting={addLaundryJob}
                  onRowRemoving={deleteLaundryJob}
                  onRowUpdating={updateLaundryJob}
                >
                  <Editing
                    mode="popup"
                    allowUpdating="true"
                    allowAdding="true"
                    allowDeleting="true"
                  >
                    <Popup
                      title="Thông tin dich vụ giặt là"
                      showTitle="true"
                      width={650}
                      height={300}
                    />
                    <Form>
                      <Item itemType="group" colCount={1} colSpan={2}>
                        <Item dataField="belonging_room_id" />
                        <Item dataField="staff_execute_id" />
                        <Item dataField="note" />
                      </Item>
                    </Form>
                  </Editing>
                  <Paging defaultPageSize={10} />
                  <Column dataField="id" caption="ID" dataType="string" />
                  <Column dataField="belonging_room_id" caption="ID phòng" />
                  <Column dataField="staff_execute_id" caption="ID nhân viên thực hiện" />
                  <Column dataField="status" caption="Trạng thái" />
                  <Column dataField="note" caption="Ghi chú" />
                  <Column dataField="created" caption="Thời gian tạo" dataType="date" />
                </DataGrid>
                {/* <MDBox pt={3}>
                  <DataTable
                    table={{ columns: pColumns, rows: pRows }}
                    isSorted={false}
                    entriesPerPage={false}
                    showTotalEntries={false}
                    noEndBorder
                  />
                </MDBox> */}
              </Card>
            </Grid>
            <Grid item xs={12}>
              <Card>
                <MDBox
                  mx={2}
                  mt={-3}
                  py={3}
                  px={2}
                  variant="gradient"
                  bgColor="info"
                  borderRadius="lg"
                  coloredShadow="info"
                >
                  <MDTypography variant="h6" color="white">
                    Danh Sách Phân Công Nhân Viên Làm Vườn
                  </MDTypography>
                </MDBox>
                <DataGrid
                  dataSource={gardeners}
                  onRowClick={detailInformation}
                  onRowInserting={addGadenerJob}
                  onRowRemoving={deleteGadenerJob}
                  onRowUpdating={updateGadenerJob}
                >
                  <Editing
                    mode="popup"
                    allowUpdating="true"
                    allowAdding="true"
                    allowDeleting="true"
                  >
                    <Popup
                      title="Thông tin phân công nhân viên làm vườn"
                      showTitle="true"
                      width={650}
                      height={250}
                    />
                    <Form>
                      <Item itemType="group" colCount={1} colSpan={2}>
                        <Item dataField="staff_execute_id" />
                        <Item dataField="note" />
                        {/* <Item dataField="Prefix" />
                        <Item dataField="BirthDate" />
                        <Item dataField="Position" />
                        <Item dataField="HireDate" /> */}
                      </Item>

                      {/* <Item itemType="group" caption="Home Address" colCount={2} colSpan={2}>
                        <Item dataField="StateID" />
                        <Item dataField="Address" />
                      </Item> */}
                    </Form>
                  </Editing>
                  {/* <Selection mode="single" /> */}
                  <Paging defaultPageSize={10} />
                  <Column dataField="id" caption="ID" dataType="string" />
                  <Column dataField="staff_execute_id" caption="ID nhân viên thực hiện" />
                  <Column dataField="note" caption="Ghi chú" />
                  <Column dataField="created" caption="Thời gian tạo" dataType="date" />
                  {/* <Column dataField="created_by_id" caption="Địa chỉ khách sạn" /> */}
                </DataGrid>
                {/* <MDBox pt={3}>
                  <DataTable
                    table={{ columns: pColumns, rows: pRows }}
                    isSorted={false}
                    entriesPerPage={false}
                    showTotalEntries={false}
                    noEndBorder
                  />
                </MDBox> */}
              </Card>
            </Grid>
            <Grid item xs={12}>
              <Card>
                <MDBox
                  mx={2}
                  mt={-3}
                  py={3}
                  px={2}
                  variant="gradient"
                  bgColor="info"
                  borderRadius="lg"
                  coloredShadow="info"
                >
                  <MDTypography variant="h6" color="white">
                    Danh Sách Phân Công Nhân Viên Hành Lí
                  </MDTypography>
                </MDBox>
                <DataGrid
                  dataSource={bellManJobs}
                  onRowClick={detailInformation}
                  onRowInserting={addBellManJob}
                  onRowRemoving={deleteBellManJob}
                  onRowUpdating={updateBellManJob}
                >
                  <Editing
                    mode="popup"
                    allowUpdating="true"
                    allowAdding="true"
                    allowDeleting="true"
                  >
                    <Popup
                      title="Thông tin phân công nhân viên hành lí"
                      showTitle="true"
                      width={650}
                      height={350}
                    />
                    <Form>
                      <Item itemType="group" colCount={1} colSpan={2}>
                        <Item dataField="belonging_room_id" />
                        <Item dataField="staff_execute_id" />
                        <Item dataField="status" />
                        <Item dataField="note" />
                        {/* <Item dataField="Prefix" />
                        <Item dataField="BirthDate" />
                        <Item dataField="Position" />
                        <Item dataField="HireDate" /> */}
                      </Item>

                      {/* <Item itemType="group" caption="Home Address" colCount={2} colSpan={2}>
                        <Item dataField="StateID" />
                        <Item dataField="Address" />
                      </Item> */}
                    </Form>
                  </Editing>
                  {/* <Selection mode="single" /> */}
                  <Paging defaultPageSize={10} />
                  <Column dataField="id" caption="ID" dataType="string" />
                  <Column dataField="belonging_room_id" caption="ID phòng" />
                  <Column dataField="staff_execute_id" caption="ID nhân viên thực hiện" />
                  <Column dataField="status" caption="Trạng thái" />
                  <Column dataField="note" caption="Ghi chú" />
                  <Column dataField="created" caption="Thời gian tạo" dataType="date" />
                  {/* <Column dataField="created_by_id" caption="Địa chỉ khách sạn" /> */}
                </DataGrid>
                {/* <MDBox pt={3}>
                  <DataTable
                    table={{ columns: pColumns, rows: pRows }}
                    isSorted={false}
                    entriesPerPage={false}
                    showTotalEntries={false}
                    noEndBorder
                  />
                </MDBox> */}
              </Card>
            </Grid>
            <Grid item xs={12}>
              <Card>
                <MDBox
                  mx={2}
                  mt={-3}
                  py={3}
                  px={2}
                  variant="gradient"
                  bgColor="info"
                  borderRadius="lg"
                  coloredShadow="info"
                >
                  <MDTypography variant="h6" color="white">
                    Danh Sách Phân Công Nhân Viên Kho Vải
                  </MDTypography>
                </MDBox>
                <DataGrid
                  dataSource={linenRoomJobs}
                  onRowClick={detailInformation}
                  onRowInserting={addLinenRoomJob}
                  onRowRemoving={deleteLinenRoomJob}
                  onRowUpdating={updateLinenRoomJob}
                >
                  <Editing
                    mode="popup"
                    allowUpdating="true"
                    allowAdding="true"
                    allowDeleting="true"
                  >
                    <Popup
                      title="Thông tin phân công nhân viên kho vải"
                      showTitle="true"
                      width={650}
                      height={400}
                    />
                    <Form>
                      <Item itemType="group" colCount={1} colSpan={2}>
                        <Item dataField="belonging_room_id" />
                        <Item dataField="staff_execute_id" />
                        {/* <Item
                          dataField="staff_laundry_id"
                          caption="ID nhân viên giặt là thực hiện"
                        /> */}
                        <Item dataField="status" />
                        <Item dataField="note" />
                        {/* <Item dataField="Prefix" />
                        <Item dataField="BirthDate" />
                        <Item dataField="Position" />
                        <Item dataField="HireDate" /> */}
                      </Item>

                      {/* <Item itemType="group" caption="Home Address" colCount={2} colSpan={2}>
                        <Item dataField="StateID" />
                        <Item dataField="Address" />
                      </Item> */}
                    </Form>
                  </Editing>
                  {/* <Selection mode="single" /> */}
                  <Paging defaultPageSize={10} />
                  <Column dataField="id" caption="ID" dataType="string" />
                  <Column dataField="belonging_room_id" caption="ID phòng" />
                  <Column dataField="staff_execute_id" caption="ID nhân viên thực hiện" />
                  <Column dataField="status" caption="Trạng thái" />
                  <Column dataField="note" caption="Ghi chú" />
                  <Column dataField="created" caption="Thời gian tạo" dataType="date" />
                  {/* <Column dataField="created_by_id" caption="Địa chỉ khách sạn" /> */}
                </DataGrid>
                {/* <MDBox pt={3}>
                  <DataTable
                    table={{ columns: pColumns, rows: pRows }}
                    isSorted={false}
                    entriesPerPage={false}
                    showTotalEntries={false}
                    noEndBorder
                  />
                </MDBox> */}
              </Card>
            </Grid>
            <Grid item xs={12}>
              <Card>
                <MDBox
                  mx={2}
                  mt={-3}
                  py={3}
                  px={2}
                  variant="gradient"
                  bgColor="info"
                  borderRadius="lg"
                  coloredShadow="info"
                >
                  <MDTypography variant="h6" color="white">
                    Danh Sách Phân Công Nhân Viên Làm Phòng
                  </MDTypography>
                </MDBox>
                <DataGrid
                  dataSource={housekeepingJobs}
                  onRowClick={detailInformation}
                  onRowInserting={addHousekeepingJobs}
                  onRowRemoving={deleteHousekeepingJobs}
                  onRowUpdating={updateHousekeepingJobs}
                >
                  <Editing
                    mode="popup"
                    allowUpdating="true"
                    allowAdding="true"
                    allowDeleting="true"
                  >
                    <Popup
                      title="Thông tin phân công nhân viên làm phòng"
                      showTitle="true"
                      width={650}
                      height={400}
                    />
                    <Form>
                      <Item itemType="group" colCount={1} colSpan={2}>
                        <Item dataField="belonging_room_id" />
                        <Item dataField="staff_execute_id" />
                        <Item dataField="room_status" />
                        <Item dataField="status" />
                        <Item dataField="note" />
                        {/* <Item dataField="Prefix" />
                        <Item dataField="BirthDate" />
                        <Item dataField="Position" />
                        <Item dataField="HireDate" /> */}
                      </Item>

                      {/* <Item itemType="group" caption="Home Address" colCount={2} colSpan={2}>
                        <Item dataField="StateID" />
                        <Item dataField="Address" />
                      </Item> */}
                    </Form>
                  </Editing>
                  {/* <Selection mode="single" /> */}
                  <Paging defaultPageSize={10} />
                  <Column dataField="id" caption="ID" dataType="string" />
                  <Column dataField="belonging_room_id" caption="ID phòng" />
                  <Column dataField="staff_execute_id" caption="ID nhân viên thực hiện" />
                  <Column dataField="room_status" caption="Trạng thái phòng" />
                  <Column dataField="status" caption="Trạng thái" />
                  <Column dataField="note" caption="Ghi chú" />
                  <Column dataField="created" caption="Thời gian tạo" dataType="date" />
                  {/* <Column dataField="created_by_id" caption="Địa chỉ khách sạn" /> */}
                </DataGrid>
                {/* <MDBox pt={3}>
                  <DataTable
                    table={{ columns: pColumns, rows: pRows }}
                    isSorted={false}
                    entriesPerPage={false}
                    showTotalEntries={false}
                    noEndBorder
                  />
                </MDBox> */}
              </Card>
            </Grid>
            <Grid item xs={12}>
              <Card>
                <MDBox
                  mx={2}
                  mt={-3}
                  py={3}
                  px={2}
                  variant="gradient"
                  bgColor="info"
                  borderRadius="lg"
                  coloredShadow="info"
                >
                  <MDTypography variant="h6" color="white">
                    Danh Sách Phân Công Nhân Viên Phục Vụ(Khu Bếp)
                  </MDTypography>
                </MDBox>
                <DataGrid
                  dataSource={waiterJobs}
                  onRowClick={detailInformation}
                  onRowInserting={addWaiterJobs}
                  onRowRemoving={deleteWaiterJobs}
                  onRowUpdating={updateWaiterJobs}
                >
                  <Editing
                    mode="popup"
                    allowUpdating="true"
                    allowAdding="true"
                    allowDeleting="true"
                  >
                    <Popup
                      title="Thông tin phân công nhân viên phục vụ"
                      showTitle="true"
                      width={650}
                      height={350}
                    />
                    <Form>
                      <Item itemType="group" colCount={1} colSpan={2}>
                        <Item dataField="belonging_room_id" />
                        <Item dataField="staff_execute_id" />
                        <Item dataField="status" />
                        <Item dataField="note" />
                        {/* <Item dataField="Prefix" />
                        <Item dataField="BirthDate" />
                        <Item dataField="Position" />
                        <Item dataField="HireDate" /> */}
                      </Item>

                      {/* <Item itemType="group" caption="Home Address" colCount={2} colSpan={2}>
                        <Item dataField="StateID" />
                        <Item dataField="Address" />
                      </Item> */}
                    </Form>
                  </Editing>
                  {/* <Selection mode="single" /> */}
                  <Paging defaultPageSize={10} />
                  <Column dataField="id" caption="ID" dataType="string" />
                  <Column dataField="belonging_room_id" caption="ID phòng" />
                  <Column dataField="staff_execute_id" caption="ID nhân viên thực hiện" />
                  <Column dataField="status" caption="Trạng thái" />
                  <Column dataField="note" caption="Ghi chú" />
                  <Column dataField="created" caption="Thời gian tạo" dataType="date" />
                  {/* <Column dataField="created_by_id" caption="Địa chỉ khách sạn" /> */}
                </DataGrid>
                {/* <MDBox pt={3}>
                  <DataTable
                    table={{ columns: pColumns, rows: pRows }}
                    isSorted={false}
                    entriesPerPage={false}
                    showTotalEntries={false}
                    noEndBorder
                  />
                </MDBox> */}
              </Card>
            </Grid>
          </Grid>
        </MDBox>
        <Footer />
      </DashboardLayout>
    );
  }
  if (localStorage.getItem("Position") === "receptionist") {
    const [receptionistNotes, setReceptionistNotes] = useState([]);

    const addReceptionistNote = (e) => {
      // console.log("ok men", e);
      fetch(`/createReceptionistDailyNote`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          number_of_check_in: e.data.number_of_check_in,
          number_of_check_out: e.data.number_of_check_out,
          note: e.data.note,
        }),
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.message === "Create successful.") {
            setSuccessSB(true);
            setSuccessMS("Thêm thành công");
          } else {
            setErrorSB(true);
            setErrorMS(data.message);
          }
        });
    };

    const deleteReceptionistNote = (e) => {
      // console.log("ok men", e.data.id);
      fetch(`/deleteReceptionistDailyNote?id=${e.data.id}`, {
        method: "POST",
        // headers: {
        //   "Content-Type": "application/json",
        // },
        // body: JSON.stringify({
        //   name: e.data.name,
        //   address: e.data.address,
        // }),
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.message === "delete successful.") {
            setSuccessSB(true);
            setSuccessMS("Xóa thành công");
          } else {
            setErrorSB(true);
            setErrorMS(data.message);
          }
        });
    };

    const updateReceptionistNote = (e) => {
      // console.log("ok men", e);
      // console.log("ok men", e.key.id);
      let newNumberOfCheckIn = e.newData.number_of_check_in;
      let newNumberOfCheckOut = e.newData.number_of_check_out;
      let newNote = e.newData.note;
      if (e.newData.number_of_check_in == null) {
        newNumberOfCheckIn = e.oldData.number_of_check_in;
      }
      if (e.newData.number_of_check_out == null) {
        newNumberOfCheckOut = e.oldData.number_of_check_out;
      }
      if (e.newData.note == null) {
        newNote = e.oldData.note;
      }
      fetch(`/updateReceptionistDailyNote?id=${e.key.id}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          number_of_check_in: newNumberOfCheckIn,
          number_of_check_out: newNumberOfCheckOut,
          note: newNote,
        }),
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.message === "Update successful.") {
            setSuccessSB(true);
            setSuccessMS("Cập nhật thành công");
          } else {
            setErrorSB(true);
            setErrorMS(data.message);
          }
        });
    };

    useEffect(() => {
      fetch("/getReceptionistInfor")
        .then((res) => res.json())
        .then((data) => {
          setReceptionistNotes(data.message);
        });
    }, []);
    return (
      <DashboardLayout>
        <DashboardNavbar />
        <MDBox pt={6} pb={3}>
          <Grid container spacing={6}>
            <Grid item xs={12}>
              <Card>
                <MDBox
                  mx={2}
                  mt={-3}
                  py={3}
                  px={2}
                  variant="gradient"
                  bgColor="info"
                  borderRadius="lg"
                  coloredShadow="info"
                >
                  <MDTypography variant="h6" color="white">
                    Ghi Chép Số Khách Đặt, Trả Phòng
                  </MDTypography>
                </MDBox>
                <DataGrid
                  dataSource={receptionistNotes}
                  onRowClick={detailInformation}
                  onRowInserting={addReceptionistNote}
                  onRowRemoving={deleteReceptionistNote}
                  onRowUpdating={updateReceptionistNote}
                >
                  <Editing
                    mode="popup"
                    allowUpdating="true"
                    allowAdding="true"
                    allowDeleting="true"
                  >
                    <Popup
                      title="Ghi Chép Số Khách Đặt, Trả Phòng"
                      showTitle="true"
                      width={650}
                      height={350}
                    />
                    <Form>
                      <Item itemType="group" colCount={1} colSpan={2}>
                        <Item dataField="number_of_check_out" />
                        <Item dataField="number_of_check_in" />
                        <Item dataField="note" />
                        {/* <Item dataField="Prefix" />
                        <Item dataField="BirthDate" />
                        <Item dataField="Position" />
                        <Item dataField="HireDate" /> */}
                        {/* <Item
                          dataField="Notes"
                          editorType="dxTextArea"
                          colSpan={2}
                          editorOptions={notesEditorOptions}
                        /> */}
                      </Item>

                      {/* <Item itemType="group" caption="Home Address" colCount={2} colSpan={2}>
                        <Item dataField="StateID" />
                        <Item dataField="Address" />
                      </Item> */}
                    </Form>
                  </Editing>
                  {/* <Selection mode="single" /> */}
                  <Paging defaultPageSize={10} />
                  <Column dataField="id" caption="ID" dataType="string" />
                  <Column dataField="number_of_check_out" caption="Số khách trả phòng" />
                  <Column dataField="number_of_check_in" caption="Số khách nhận phòng" />
                  <Column dataField="note" caption="Ghi chú" />
                  <Column dataField="created" caption="Ngày tạo ghi chép" />
                </DataGrid>
                {renderSuccessSB}
                {renderErrorSB}
                {/* <MDBox
                  mx={2}
                  mt={-3}
                  py={3}
                  px={2}
                  variant="gradient"
                  bgColor="info"
                  borderRadius="lg"
                  coloredShadow="info"
                >
                  <MDTypography variant="h6" color="white">
                    Authors Table
                  </MDTypography>
                </MDBox>
                <MDBox pt={3}>
                  <DataTable
                    table={{ columns, rows }}
                    isSorted={false}
                    entriesPerPage={false}
                    showTotalEntries={false}
                    noEndBorder
                  />
                </MDBox> */}
              </Card>
            </Grid>
          </Grid>
        </MDBox>
        <Footer />
      </DashboardLayout>
    );
  }
}

export default Tables;
