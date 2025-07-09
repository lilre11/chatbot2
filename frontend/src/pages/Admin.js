import React, { useState, useEffect } from 'react';
import { Row, Col, Card, Tab, Nav, Table, Badge, Form } from 'react-bootstrap';
import axios from 'axios';

const Admin = () => {
  const [systemStatus, setSystemStatus] = useState({});
  const [statistics, setStatistics] = useState({});
  const [logs, setLogs] = useState([]);
  const [users, setUsers] = useState([]);
  const [logLevelFilter, setLogLevelFilter] = useState('');

  useEffect(() => {
    loadSystemStatus();
    loadStatistics();
    loadLogs();
    loadUsers();

    // Auto-refresh every 30 seconds
    const interval = setInterval(() => {
      loadSystemStatus();
      loadStatistics();
    }, 30000);

    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    loadLogs();
  }, [logLevelFilter]);

  const loadSystemStatus = async () => {
    try {
      const response = await axios.get('/api/admin/status');
      setSystemStatus(response.data);
    } catch (error) {
      console.error('Error loading system status:', error);
      setSystemStatus({
        database: { status: 'error', healthy: false },
        ai_service: { status: 'error', healthy: false },
        overall_status: 'error'
      });
    }
  };

  const loadStatistics = async () => {
    try {
      const response = await axios.get('/api/admin/stats');
      setStatistics(response.data);
    } catch (error) {
      console.error('Error loading statistics:', error);
    }
  };

  const loadLogs = async () => {
    try {
      const url = logLevelFilter ? `/api/admin/logs?level=${logLevelFilter}` : '/api/admin/logs';
      const response = await axios.get(url);
      setLogs(response.data.logs);
    } catch (error) {
      console.error('Error loading logs:', error);
    }
  };

  const loadUsers = async () => {
    try {
      const response = await axios.get('/api/admin/users');
      setUsers(response.data.users);
    } catch (error) {
      console.error('Error loading users:', error);
    }
  };

  const getStatusBadgeVariant = (healthy) => {
    return healthy ? 'success' : 'danger';
  };

  const getStatusText = (healthy) => {
    return healthy ? 'Healthy' : 'Error';
  };

  const getLogLevelVariant = (level) => {
    switch (level) {
      case 'ERROR': return 'danger';
      case 'WARNING': return 'warning';
      case 'INFO': return 'info';
      default: return 'secondary';
    }
  };

  const formatTimestamp = (timestamp) => {
    return new Date(timestamp).toLocaleString();
  };

  const formatNumber = (num) => {
    return typeof num === 'number' ? num.toLocaleString() : '-';
  };

  return (
    <div>
      <Row>
        <Col>
          <h2 className="mb-4">
            <i className="fas fa-cogs me-2"></i>
            Admin Dashboard
          </h2>
        </Col>
      </Row>

      {/* System Status */}
      <Row className="mb-4">
        <Col>
          <Card>
            <Card.Header>
              <h5 className="mb-0">
                <i className="fas fa-heartbeat me-2"></i>
                System Status
              </h5>
            </Card.Header>
            <Card.Body>
              <Row>
                <Col md={4}>
                  <Card className="bg-light">
                    <Card.Body className="text-center">
                      <i className={`fas fa-database fa-2x mb-2 ${systemStatus.database?.healthy ? 'text-success' : 'text-danger'}`}></i>
                      <h6>Database</h6>
                      <Badge variant={getStatusBadgeVariant(systemStatus.database?.healthy)}>
                        {getStatusText(systemStatus.database?.healthy)}
                      </Badge>
                    </Card.Body>
                  </Card>
                </Col>
                <Col md={4}>
                  <Card className="bg-light">
                    <Card.Body className="text-center">
                      <i className={`fas fa-brain fa-2x mb-2 ${systemStatus.ai_service?.healthy ? 'text-success' : 'text-danger'}`}></i>
                      <h6>AI Service</h6>
                      <Badge variant={getStatusBadgeVariant(systemStatus.ai_service?.healthy)}>
                        {getStatusText(systemStatus.ai_service?.healthy)}
                      </Badge>
                    </Card.Body>
                  </Card>
                </Col>
                <Col md={4}>
                  <Card className="bg-light">
                    <Card.Body className="text-center">
                      <i className={`fas fa-server fa-2x mb-2 ${systemStatus.overall_status === 'healthy' ? 'text-success' : 'text-danger'}`}></i>
                      <h6>Overall</h6>
                      <Badge variant={systemStatus.overall_status === 'healthy' ? 'success' : 'danger'}>
                        {systemStatus.overall_status === 'healthy' ? 'Healthy' : 'Error'}
                      </Badge>
                    </Card.Body>
                  </Card>
                </Col>
              </Row>
            </Card.Body>
          </Card>
        </Col>
      </Row>

      {/* Statistics */}
      <Row className="mb-4">
        <Col md={3}>
          <Card className="bg-primary text-white">
            <Card.Body>
              <div className="d-flex justify-content-between">
                <div>
                  <h3>{formatNumber(statistics.users)}</h3>
                  <p className="mb-0">Users</p>
                </div>
                <div className="align-self-center">
                  <i className="fas fa-users fa-2x"></i>
                </div>
              </div>
            </Card.Body>
          </Card>
        </Col>
        <Col md={3}>
          <Card className="bg-success text-white">
            <Card.Body>
              <div className="d-flex justify-content-between">
                <div>
                  <h3>{formatNumber(statistics.conversations)}</h3>
                  <p className="mb-0">Conversations</p>
                </div>
                <div className="align-self-center">
                  <i className="fas fa-comments fa-2x"></i>
                </div>
              </div>
            </Card.Body>
          </Card>
        </Col>
        <Col md={3}>
          <Card className="bg-info text-white">
            <Card.Body>
              <div className="d-flex justify-content-between">
                <div>
                  <h3>{formatNumber(statistics.messages)}</h3>
                  <p className="mb-0">Messages</p>
                </div>
                <div className="align-self-center">
                  <i className="fas fa-envelope fa-2x"></i>
                </div>
              </div>
            </Card.Body>
          </Card>
        </Col>
        <Col md={3}>
          <Card className="bg-warning text-white">
            <Card.Body>
              <div className="d-flex justify-content-between">
                <div>
                  <h3>{formatNumber(statistics.active_conversations_24h)}</h3>
                  <p className="mb-0">Active (24h)</p>
                </div>
                <div className="align-self-center">
                  <i className="fas fa-chart-line fa-2x"></i>
                </div>
              </div>
            </Card.Body>
          </Card>
        </Col>
      </Row>

      {/* Tabs */}
      <Row>
        <Col>
          <Tab.Container defaultActiveKey="logs">
            <Nav variant="tabs">
              <Nav.Item>
                <Nav.Link eventKey="logs">
                  <i className="fas fa-list me-1"></i>
                  System Logs
                </Nav.Link>
              </Nav.Item>
              <Nav.Item>
                <Nav.Link eventKey="users">
                  <i className="fas fa-users me-1"></i>
                  Users
                </Nav.Link>
              </Nav.Item>
            </Nav>

            <Tab.Content className="mt-3">
              {/* Logs Tab */}
              <Tab.Pane eventKey="logs">
                <Card>
                  <Card.Header className="d-flex justify-content-between align-items-center">
                    <h6 className="mb-0">System Logs</h6>
                    <Form.Select
                      size="sm"
                      style={{ width: 'auto' }}
                      value={logLevelFilter}
                      onChange={(e) => setLogLevelFilter(e.target.value)}
                    >
                      <option value="">All Levels</option>
                      <option value="INFO">Info</option>
                      <option value="WARNING">Warning</option>
                      <option value="ERROR">Error</option>
                    </Form.Select>
                  </Card.Header>
                  <Card.Body className="p-0">
                    <div className="table-responsive">
                      <Table striped className="mb-0">
                        <thead className="table-dark">
                          <tr>
                            <th>Timestamp</th>
                            <th>Level</th>
                            <th>Module</th>
                            <th>Message</th>
                          </tr>
                        </thead>
                        <tbody>
                          {logs.length === 0 ? (
                            <tr>
                              <td colSpan="4" className="text-center text-muted py-4">
                                No logs found
                              </td>
                            </tr>
                          ) : (
                            logs.map((log, index) => (
                              <tr key={index}>
                                <td>{formatTimestamp(log.timestamp)}</td>
                                <td>
                                  <Badge variant={getLogLevelVariant(log.level)}>
                                    {log.level}
                                  </Badge>
                                </td>
                                <td>{log.module || '-'}</td>
                                <td>{log.message}</td>
                              </tr>
                            ))
                          )}
                        </tbody>
                      </Table>
                    </div>
                  </Card.Body>
                </Card>
              </Tab.Pane>

              {/* Users Tab */}
              <Tab.Pane eventKey="users">
                <Card>
                  <Card.Header>
                    <h6 className="mb-0">Recent Users</h6>
                  </Card.Header>
                  <Card.Body className="p-0">
                    <div className="table-responsive">
                      <Table striped className="mb-0">
                        <thead className="table-dark">
                          <tr>
                            <th>ID</th>
                            <th>Username</th>
                            <th>Email</th>
                            <th>Created</th>
                            <th>Status</th>
                          </tr>
                        </thead>
                        <tbody>
                          {users.length === 0 ? (
                            <tr>
                              <td colSpan="5" className="text-center text-muted py-4">
                                No users found
                              </td>
                            </tr>
                          ) : (
                            users.map((user, index) => (
                              <tr key={index}>
                                <td>{user.id}</td>
                                <td>{user.username}</td>
                                <td>{user.email}</td>
                                <td>{formatTimestamp(user.created_at)}</td>
                                <td>
                                  <Badge variant={user.is_active ? 'success' : 'secondary'}>
                                    {user.is_active ? 'Active' : 'Inactive'}
                                  </Badge>
                                </td>
                              </tr>
                            ))
                          )}
                        </tbody>
                      </Table>
                    </div>
                  </Card.Body>
                </Card>
              </Tab.Pane>
            </Tab.Content>
          </Tab.Container>
        </Col>
      </Row>
    </div>
  );
};

export default Admin;
