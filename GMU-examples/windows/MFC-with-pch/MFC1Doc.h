// MFC1Doc.h : interface of the CMFC1Doc class
//
/////////////////////////////////////////////////////////////////////////////

#if !defined(AFX_MFC1DOC_H__5282DAF3_6B2D_4013_B561_D80D20F4DFD9__INCLUDED_)
#define AFX_MFC1DOC_H__5282DAF3_6B2D_4013_B561_D80D20F4DFD9__INCLUDED_

#if _MSC_VER > 1000
#pragma once
#endif // _MSC_VER > 1000


class CMFC1Doc : public CDocument
{
protected: // create from serialization only
	CMFC1Doc();
	DECLARE_DYNCREATE(CMFC1Doc)

// Attributes
public:

// Operations
public:

// Overrides
	// ClassWizard generated virtual function overrides
	//{{AFX_VIRTUAL(CMFC1Doc)
	public:
	virtual BOOL OnNewDocument();
	virtual void Serialize(CArchive& ar);
	//}}AFX_VIRTUAL

// Implementation
public:
	virtual ~CMFC1Doc();
#ifdef _DEBUG
	virtual void AssertValid() const;
	virtual void Dump(CDumpContext& dc) const;
#endif

protected:

// Generated message map functions
protected:
	//{{AFX_MSG(CMFC1Doc)
		// NOTE - the ClassWizard will add and remove member functions here.
		//    DO NOT EDIT what you see in these blocks of generated code !
	//}}AFX_MSG
	DECLARE_MESSAGE_MAP()
};

/////////////////////////////////////////////////////////////////////////////

//{{AFX_INSERT_LOCATION}}
// Microsoft Visual C++ will insert additional declarations immediately before the previous line.

#endif // !defined(AFX_MFC1DOC_H__5282DAF3_6B2D_4013_B561_D80D20F4DFD9__INCLUDED_)
