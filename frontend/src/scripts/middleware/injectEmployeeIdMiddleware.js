export function injectEmployeeIdMiddleware(req, res, next) {
    const employeeId = localStorage.getItem('employee_id'); 
    console.log('Employee ID:', employeeId);
    if (employeeId) {
      req.headers['employee_id'] = employeeId;
    }
  
    next();
  };
  